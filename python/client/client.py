import os
import yaml
import grpc
from pathlib import Path
from datetime import datetime
import gzip
from typing import List, Dict, Optional, Union, Iterator

from ...generated import client_storage_pb2 as pb
from ...generated import client_storage_pb2_grpc as pb_grpc
from .retry import retry

class ACSClient:
    """Client for Accelerated Cloud Storage service."""
    
    SERVER_ADDRESS = "acceleratedcloudstorages3cache.com:50050"
    CHUNK_SIZE = 64 * 1024  # 64KB chunks for streaming
    COMPRESSION_THRESHOLD = 1 * 1024 * 1024  # 1MB threshold for compression

    def __init__(self):
        """Initialize the ACS client with authentication and connection setup."""
        # Setup secure channel
        creds = grpc.ssl_channel_credentials()
        options = [
            ('grpc.max_send_message_length', 1024 * 1024 * 1024),  # 1GB
            ('grpc.max_receive_message_length', 1024 * 1024 * 1024),  # 1GB
            ('grpc.keepalive_time_ms', 20000),  # 20 seconds
            ('grpc.keepalive_timeout_ms', 60000),  # 60 seconds
        ]
        
        self.channel = grpc.secure_channel(self.SERVER_ADDRESS, creds, options=options)
        self.client = pb_grpc.ObjectStorageCacheStub(self.channel)
        
        # Load and authenticate
        creds = self._load_credentials()
        self._authenticate(creds)
        self._check_key_rotation(creds)

    def close(self):
        """Close the gRPC channel."""
        self.channel.close()

    def _load_credentials(self) -> dict:
        """Load credentials from ~/.acs/credentials.yaml file."""
        creds_path = Path.home() / '.acs' / 'credentials.yaml'
        
        # Create directory if needed
        creds_path.parent.mkdir(mode=0o700, exist_ok=True)
        
        # Create default credentials if file doesn't exist
        if not creds_path.exists():
            default_creds = {
                'default': {
                    'access_key_id': 'your_access_key_id',
                    'secret_access_key': 'your_secret_access_key'
                }
            }
            with open(creds_path, 'w') as f:
                yaml.dump(default_creds, f)
        
        # Load credentials
        with open(creds_path) as f:
            profiles = yaml.safe_load(f)
        
        profile = os.getenv('ACS_PROFILE', 'default')
        if profile not in profiles:
            raise ValueError(f"Profile '{profile}' not found in credentials file")
            
        return profiles[profile]

    def _authenticate(self, creds: dict):
        """Authenticate with the ACS service."""
        request = pb.AuthRequest(
            access_key_id=creds['access_key_id'],
            secret_access_key=creds['secret_access_key']
        )
        self.client.Authenticate(request)

    def _check_key_rotation(self, creds: dict):
        """Check if key rotation is needed."""
        try:
            self.rotate_key(False)
        except Exception as e:
            print(f"Warning: Key rotation check failed: {e}")

    @retry()
    def create_bucket(self, bucket: str, region: str) -> None:
        """Create a new bucket in the specified region."""
        request = pb.CreateBucketRequest(bucket=bucket, region=region)
        try:
            self.client.CreateBucket(request)
        except grpc.RpcError as e:
            raise BucketError(f"Failed to create bucket: {e.details()}") from e

    @retry()
    def delete_bucket(self, bucket: str) -> None:
        """Delete a bucket."""
        request = pb.DeleteBucketRequest(bucket=bucket)
        self.client.DeleteBucket(request)

    @retry()
    def list_buckets(self) -> List[pb.Bucket]:
        """List all buckets."""
        request = pb.ListBucketsRequest()
        response = self.client.ListBuckets(request)
        return list(response.buckets)

    @retry()
    def put_object(self, bucket: str, key: str, data: bytes) -> None:
        """Upload data to a bucket."""
        # Check if compression would be beneficial
        is_compressed = False
        if len(data) >= self.COMPRESSION_THRESHOLD:
            compressed = gzip.compress(data, compresslevel=1)  # Fastest compression
            if len(compressed) < len(data):
                data = compressed
                is_compressed = True

        def request_generator():
            # Send parameters first
            yield pb.PutObjectRequest(
                parameters=pb.PutObjectInput(
                    bucket=bucket,
                    key=key,
                    isCompressed=is_compressed
                )
            )
            
            # Send data chunks
            for i in range(0, len(data), self.CHUNK_SIZE):
                chunk = data[i:i + self.CHUNK_SIZE]
                yield pb.PutObjectRequest(chunk=chunk)

        self.client.PutObject(request_generator())

    @retry()
    def get_object(self, bucket: str, key: str) -> bytes:
        """Download an object from a bucket."""
        try:
            request = pb.GetObjectRequest(bucket=bucket, key=key)
            response_stream = self.client.GetObject(request)
            
            # Skip metadata message and collect chunks
            first_message = True
            chunks = []
            for response in response_stream:
                if first_message:
                    first_message = False
                    continue
                if response.HasField('chunk'):
                    chunks.append(response.chunk)
            
            return b''.join(chunks)
        except grpc.RpcError as e:
            raise ObjectError(f"Failed to get object: {e.details()}") from e

    @retry()
    def delete_object(self, bucket: str, key: str) -> None:
        """Delete a single object from a bucket."""
        try:
            request = pb.DeleteObjectRequest(bucket=bucket, key=key)
            self.client.DeleteObject(request)
        except grpc.RpcError as e:
            raise ObjectError(f"Failed to delete object: {e.details()}") from e

    def delete_objects(self, bucket: str, keys: List[str]) -> None:
        """Delete multiple objects from a bucket."""
        try:
            objects = [pb.ObjectIdentifier(key=key) for key in keys]
            request = pb.DeleteObjectsRequest(bucket=bucket, objects=objects)
            response = self.client.DeleteObjects(request)
            
            if len(response.deletedObjects) != len(keys):
                raise ObjectError("Some objects failed to delete")
        except grpc.RpcError as e:
            raise ObjectError(f"Failed to delete objects: {e.details()}") from e

    def head_object(self, bucket: str, key: str) -> HeadObjectOutput:
        """Get object metadata without downloading the object."""
        try:
            request = pb.HeadObjectRequest(bucket=bucket, key=key)
            response = self.client.HeadObject(request)
            
            return HeadObjectOutput(
                content_type=response.metadata.content_type,
                content_encoding=response.metadata.content_encoding,
                content_language=response.metadata.content_language,
                content_length=response.metadata.size,
                last_modified=response.metadata.last_modified.ToDatetime(),
                etag=response.metadata.etag,
                user_metadata=response.metadata.user_metadata,
                server_side_encryption=response.metadata.server_side_encryption,
                version_id=response.metadata.version_id
            )
        except grpc.RpcError as e:
            raise ObjectError(f"Failed to get object metadata: {e.details()}") from e

    def list_objects(self, bucket: str, options: Optional[ListObjectsOptions] = None) -> Iterator[str]:
        """List objects in a bucket with optional filtering."""
        try:
            request = pb.ListObjectsRequest(bucket=bucket)
            if options:
                if options.prefix:
                    request.prefix = options.prefix
                if options.start_after:
                    request.start_after = options.start_after
                if options.max_keys:
                    request.max_keys = options.max_keys

            response_stream = self.client.ListObjects(request)
            for response in response_stream:
                if response.HasField('object'):
                    yield response.object.key
        except grpc.RpcError as e:
            raise BucketError(f"Failed to list objects: {e.details()}") from e

    def copy_object(self, bucket: str, copy_source: str, key: str) -> None:
        """Copy an object within or between buckets."""
        try:
            request = pb.CopyObjectRequest(
                bucket=bucket,
                copySource=copy_source,
                key=key
            )
            self.client.CopyObject(request)
        except grpc.RpcError as e:
            raise ObjectError(f"Failed to copy object: {e.details()}") from e

    def head_bucket(self, bucket: str) -> HeadBucketOutput:
        """Get bucket metadata."""
        try:
            request = pb.HeadBucketRequest(bucket=bucket)
            response = self.client.HeadBucket(request)
            return HeadBucketOutput(region=response.bucketRegion)
        except grpc.RpcError as e:
            raise BucketError(f"Failed to get bucket metadata: {e.details()}") from e

    def rotate_key(self, force: bool = False) -> None:
        """Rotate access keys if needed or forced."""
        try:
            creds = self._load_credentials()
            request = pb.RotateKeyRequest(
                access_key_id=creds['access_key_id'],
                force=force
            )
            response = self.client.RotateKey(request)
            
            if response.rotated:
                self._update_credentials(response.new_secret_access_key)
        except grpc.RpcError as e:
            raise ConfigurationError(f"Failed to rotate key: {e.details()}") from e

    def _update_credentials(self, new_secret_key: str) -> None:
        """Update credentials file with new secret key."""
        creds_path = Path.home() / '.acs' / 'credentials.yaml'
        profile = os.getenv('ACS_PROFILE', 'default')
        
        with open(creds_path) as f:
            profiles = yaml.safe_load(f)
        
        profiles[profile]['secret_access_key'] = new_secret_key
        
        with open(creds_path, 'w') as f:
            yaml.dump(profiles, f)

    def share_bucket(self, bucket: str) -> None:
        """Share a bucket with the service."""
        try:
            request = pb.ShareBucketRequest(bucketName=bucket)
            self.client.ShareBucket(request)
        except grpc.RpcError as e:
            raise BucketError(f"Failed to share bucket: {e.details()}") from e
