# Copyright 2025 Accelerated Cloud Storage Corporation. All Rights Reserved.
import os
import yaml
import grpc
from pathlib import Path
from datetime import datetime
import gzip
from typing import List, Dict, Optional, Union, Iterator
from dataclasses import dataclass
from acs_sdk.internal.generated import client_storage_pb2 as pb
from acs_sdk.internal.generated import client_storage_pb2_grpc as pb_grpc
from .retry import retry
from .types import *
from .exceptions import *

class ACSClient:
    """
    ACSClient is a client for the Accelerated Cloud Storage (ACS) service. It provides methods to interact with the ACS service, including creating, deleting, and listing buckets and objects, as well as uploading and downloading data.
    """
    
    # Constants 
    SERVER_ADDRESS = "acceleratedcloudstorages3cache.com:50050"
    CHUNK_SIZE = 64 * 1024  # 64KB chunks for streaming
    COMPRESSION_THRESHOLD = 100 * 1024 * 1024  # 100MB threshold for compression

    def __init__(self):
        """Initialize the ACSClient.

        Sets up a secure gRPC channel, loads credentials, authenticates,
        and checks for key rotation.
        """
        # Setup secure channel
        creds = grpc.ssl_channel_credentials()
        options = [
            ('grpc.max_send_message_length', 1024 * 1024 * 1024),  # 1GB
            ('grpc.max_receive_message_length', 1024 * 1024 * 1024),  # 1GB
            ('grpc.keepalive_time_ms', 20000),  # 20 seconds
            ('grpc.keepalive_timeout_ms', 60000),  # 60 seconds
            ('grpc.http2.max_pings_without_data', 0),
            ('grpc.http2.min_time_between_pings_ms', 10000),
            ('grpc.http2.min_ping_interval_without_data_ms', 5000),
        ]
        
        self.channel = grpc.secure_channel(self.SERVER_ADDRESS, creds, options=options)
        self.client = pb_grpc.ObjectStorageCacheStub(self.channel)
        
        # Load and authenticate
        creds = self._load_credentials()
        self._authenticate(creds)
        self._check_key_rotation(creds)

    def close(self):
        """Close the client."""
        self.channel.close()

    def _load_credentials(self) -> dict:
        """Load credentials from ~/.acs/credentials.yaml.

        Creates the credentials file with default values if it does not exist.

        Returns:
            dict: The credentials for the active profile.

        Raises:
            ValueError: If the active profile is not found in the credentials.
        """
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
        """Authenticate with the ACS service.

        Args:
            creds (dict): The credentials containing access and secret keys.
        """
        request = pb.AuthRequest(
            access_key_id=creds['access_key_id'],
            secret_access_key=creds['secret_access_key']
        )
        self.client.Authenticate(request)

    def _check_key_rotation(self, creds: dict):
        """Check and perform key rotation if necessary.

        Args:
            creds (dict): The credentials used for authentication.
        """
        try:
            self.rotate_key(False)
        except Exception as e:
            print(f"Warning: Key rotation check failed: {e}")

    @retry()
    def create_bucket(self, bucket: str, region: str) -> None:
        """Create a new bucket in the specified region.

        Args:
            bucket (str): The bucket name.
            region (str): The region in which to create the bucket.

        Raises:
            BucketError: If bucket creation fails.
        """
        request = pb.CreateBucketRequest(bucket=bucket, region=region)
        try:
            self.client.CreateBucket(request)
        except grpc.RpcError as e:
            raise BucketError(f"Failed to create bucket: {e.details()}") from e

    @retry()
    def delete_bucket(self, bucket: str) -> None:
        """Delete a bucket.

        Args:
            bucket (str): The bucket name.
        """
        request = pb.DeleteBucketRequest(bucket=bucket)
        self.client.DeleteBucket(request)

    @retry()
    def list_buckets(self) -> List[pb.Bucket]:
        """List all buckets.

        Returns:
            List[pb.Bucket]: A list of buckets.
        """
        request = pb.ListBucketsRequest()
        response = self.client.ListBuckets(request)
        return list(response.buckets)

    @retry()
    def put_object(self, bucket: str, key: str, data: bytes) -> None:
        """Upload data to a bucket with optional compression.

        Args:
            bucket (str): The bucket name.
            key (str): The object key.
            data (bytes): The data to upload.
        """
        is_compressed = False
        if len(data) >= self.COMPRESSION_THRESHOLD:
            compressed = gzip.compress(data, compresslevel=1)
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
        """Download an object from a bucket.

        Args:
            bucket (str): The bucket name.
            key (str): The object key.

        Returns:
            bytes: The downloaded object data.

        Raises:
            ObjectError: If retrieval fails.
        """
        try:
            request = pb.GetObjectRequest(bucket=bucket, key=key)
            response_stream = self.client.GetObject(request)
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
        """Delete a single object from a bucket.

        Args:
            bucket (str): The bucket name.
            key (str): The object key.

        Raises:
            ObjectError: If deletion fails.
        """
        try:
            request = pb.DeleteObjectRequest(bucket=bucket, key=key)
            self.client.DeleteObject(request)
        except grpc.RpcError as e:
            raise ObjectError(f"Failed to delete object: {e.details()}") from e

    @retry()
    def delete_objects(self, bucket: str, keys: List[str]) -> None:
        """Delete multiple objects from a bucket.

        Args:
            bucket (str): The bucket name.
            keys (List[str]): A list of object keys to delete.

        Raises:
            ObjectError: If deletion fails.
        """
        try:
            objects = [pb.ObjectIdentifier(key=key) for key in keys]
            request = pb.DeleteObjectsRequest(bucket=bucket, objects=objects)
            response = self.client.DeleteObjects(request)
            
            if len(response.deletedObjects) != len(keys):
                raise ObjectError("Some objects failed to delete")
        except grpc.RpcError as e:
            raise ObjectError(f"Failed to delete objects: {e.details()}") from e
    
    @retry()
    def head_object(self, bucket: str, key: str) -> HeadObjectOutput:
        """Retrieve metadata for an object without downloading it.

        Args:
            bucket (str): The bucket name.
            key (str): The object key.

        Returns:
            HeadObjectOutput: The metadata of the object.

        Raises:
            ObjectError: If metadata retrieval fails.
        """
        try:
            request = pb.HeadObjectRequest(bucket=bucket, key=key)
            print("Sending head object request")
            response = self.client.HeadObject(request)
            
            if not response or not response.metadata:
                raise ObjectError("No metadata received", operation="HEAD")
            
            return HeadObjectOutput(
                content_type=getattr(response.metadata, 'content_type', ''),
                content_encoding=getattr(response.metadata, 'content_encoding', None),
                content_language=getattr(response.metadata, 'content_language', None),
                content_length=getattr(response.metadata, 'size', 0),
                last_modified=getattr(response.metadata, 'last_modified', datetime.now()).ToDatetime(),
                etag=getattr(response.metadata, 'etag', ''),
                user_metadata=getattr(response.metadata, 'user_metadata', {}),
                server_side_encryption=getattr(response.metadata, 'server_side_encryption', None),
                version_id=getattr(response.metadata, 'version_id', None)
            )
        except grpc.RpcError as e:
            raise ObjectError(f"Failed to get object metadata: {e.details()}", operation="HEAD") from e
        except Exception as e:
            raise ObjectError(f"Unexpected error in head_object: {str(e)}", operation="HEAD") from e
    
    @retry()
    def list_objects(self, bucket: str, options: Optional[ListObjectsOptions] = None) -> Iterator[str]:
        """List objects in a bucket with optional filtering.

        Args:
            bucket (str): The bucket name.
            options (Optional[ListObjectsOptions], optional): Filtering options.

        Yields:
            Iterator[str]: Object keys.
        
        Raises:
            BucketError: If listing fails.
        """
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
    
    @retry()
    def copy_object(self, bucket: str, copy_source: str, key: str) -> None:
        """Copy an object within or between buckets.

        Args:
            bucket (str): The destination bucket name.
            copy_source (str): The source object identifier.
            key (str): The destination object key.

        Raises:
            ObjectError: If the copy operation fails.
        """
        try:
            request = pb.CopyObjectRequest(
                bucket=bucket,
                copySource=copy_source,
                key=key
            )
            self.client.CopyObject(request)
        except grpc.RpcError as e:
            raise ObjectError(f"Failed to copy object: {e.details()}") from e
    
    @retry()
    def head_bucket(self, bucket: str) -> HeadBucketOutput:
        """Retrieve metadata for a bucket.

        Args:
            bucket (str): The bucket name.

        Returns:
            HeadBucketOutput: Bucket metadata including region.

        Raises:
            BucketError: If the operation fails.
        """
        try:
            request = pb.HeadBucketRequest(bucket=bucket)
            response = self.client.HeadBucket(request)
            return HeadBucketOutput(region=response.bucketRegion)
        except grpc.RpcError as e:
            raise BucketError(f"Failed to get bucket metadata: {e.details()}") from e

    @retry()
    def rotate_key(self, force: bool = False) -> None:
        """Rotate access keys.

        Args:
            force (bool, optional): Whether to force key rotation even if not needed.

        Raises:
            ConfigurationError: If key rotation fails.
        """
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
        """Update the stored credentials with a new secret key.

        Args:
            new_secret_key (str): The new secret access key.
        """
        creds_path = Path.home() / '.acs' / 'credentials.yaml'
        profile = os.getenv('ACS_PROFILE', 'default')
        
        with open(creds_path) as f:
            profiles = yaml.safe_load(f)
        
        profiles[profile]['secret_access_key'] = new_secret_key
        
        with open(creds_path, 'w') as f:
            yaml.dump(profiles, f)

    @retry()
    def share_bucket(self, bucket: str) -> None:
        """Share a bucket with the ACS service.

        Args:
            bucket (str): The bucket name.

        Raises:
            BucketError: If sharing fails.
        """
        try:
            request = pb.ShareBucketRequest(bucketName=bucket)
            self.client.ShareBucket(request)
        except grpc.RpcError as e:
            raise BucketError(f"Failed to share bucket: {e.details()}") from e
