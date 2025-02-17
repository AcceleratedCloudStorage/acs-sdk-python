# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

import client_storage_pb2 as client__storage__pb2

GRPC_GENERATED_VERSION = '1.70.0'
GRPC_VERSION = grpc.__version__
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    raise RuntimeError(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in client_storage_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class ObjectStorageCacheStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.CreateBucket = channel.unary_unary(
                '/proto.ObjectStorageCache/CreateBucket',
                request_serializer=client__storage__pb2.CreateBucketRequest.SerializeToString,
                response_deserializer=client__storage__pb2.CreateBucketResponse.FromString,
                _registered_method=True)
        self.DeleteBucket = channel.unary_unary(
                '/proto.ObjectStorageCache/DeleteBucket',
                request_serializer=client__storage__pb2.DeleteBucketRequest.SerializeToString,
                response_deserializer=client__storage__pb2.DeleteBucketResponse.FromString,
                _registered_method=True)
        self.ListBuckets = channel.unary_unary(
                '/proto.ObjectStorageCache/ListBuckets',
                request_serializer=client__storage__pb2.ListBucketsRequest.SerializeToString,
                response_deserializer=client__storage__pb2.ListBucketsResponse.FromString,
                _registered_method=True)
        self.HeadBucket = channel.unary_unary(
                '/proto.ObjectStorageCache/HeadBucket',
                request_serializer=client__storage__pb2.HeadBucketRequest.SerializeToString,
                response_deserializer=client__storage__pb2.HeadBucketResponse.FromString,
                _registered_method=True)
        self.PutObject = channel.stream_unary(
                '/proto.ObjectStorageCache/PutObject',
                request_serializer=client__storage__pb2.PutObjectRequest.SerializeToString,
                response_deserializer=client__storage__pb2.PutObjectResponse.FromString,
                _registered_method=True)
        self.GetObject = channel.unary_stream(
                '/proto.ObjectStorageCache/GetObject',
                request_serializer=client__storage__pb2.GetObjectRequest.SerializeToString,
                response_deserializer=client__storage__pb2.GetObjectResponse.FromString,
                _registered_method=True)
        self.DeleteObject = channel.unary_unary(
                '/proto.ObjectStorageCache/DeleteObject',
                request_serializer=client__storage__pb2.DeleteObjectRequest.SerializeToString,
                response_deserializer=client__storage__pb2.DeleteObjectResponse.FromString,
                _registered_method=True)
        self.DeleteObjects = channel.unary_unary(
                '/proto.ObjectStorageCache/DeleteObjects',
                request_serializer=client__storage__pb2.DeleteObjectsRequest.SerializeToString,
                response_deserializer=client__storage__pb2.DeleteObjectsResponse.FromString,
                _registered_method=True)
        self.CopyObject = channel.unary_unary(
                '/proto.ObjectStorageCache/CopyObject',
                request_serializer=client__storage__pb2.CopyObjectRequest.SerializeToString,
                response_deserializer=client__storage__pb2.CopyObjectResponse.FromString,
                _registered_method=True)
        self.HeadObject = channel.unary_unary(
                '/proto.ObjectStorageCache/HeadObject',
                request_serializer=client__storage__pb2.HeadObjectRequest.SerializeToString,
                response_deserializer=client__storage__pb2.HeadObjectResponse.FromString,
                _registered_method=True)
        self.ListObjects = channel.unary_stream(
                '/proto.ObjectStorageCache/ListObjects',
                request_serializer=client__storage__pb2.ListObjectsRequest.SerializeToString,
                response_deserializer=client__storage__pb2.ListObjectsResponse.FromString,
                _registered_method=True)
        self.Authenticate = channel.unary_unary(
                '/proto.ObjectStorageCache/Authenticate',
                request_serializer=client__storage__pb2.AuthRequest.SerializeToString,
                response_deserializer=client__storage__pb2.AuthResponse.FromString,
                _registered_method=True)
        self.RotateKey = channel.unary_unary(
                '/proto.ObjectStorageCache/RotateKey',
                request_serializer=client__storage__pb2.RotateKeyRequest.SerializeToString,
                response_deserializer=client__storage__pb2.RotateKeyResponse.FromString,
                _registered_method=True)
        self.ShareBucket = channel.unary_unary(
                '/proto.ObjectStorageCache/ShareBucket',
                request_serializer=client__storage__pb2.ShareBucketRequest.SerializeToString,
                response_deserializer=client__storage__pb2.ShareBucketResponse.FromString,
                _registered_method=True)


class ObjectStorageCacheServicer(object):
    """Missing associated documentation comment in .proto file."""

    def CreateBucket(self, request, context):
        """Bucket operations
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteBucket(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ListBuckets(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def HeadBucket(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def PutObject(self, request_iterator, context):
        """Object operations
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetObject(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteObject(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteObjects(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CopyObject(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def HeadObject(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ListObjects(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Authenticate(self, request, context):
        """Configuration operations 
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def RotateKey(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ShareBucket(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ObjectStorageCacheServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'CreateBucket': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateBucket,
                    request_deserializer=client__storage__pb2.CreateBucketRequest.FromString,
                    response_serializer=client__storage__pb2.CreateBucketResponse.SerializeToString,
            ),
            'DeleteBucket': grpc.unary_unary_rpc_method_handler(
                    servicer.DeleteBucket,
                    request_deserializer=client__storage__pb2.DeleteBucketRequest.FromString,
                    response_serializer=client__storage__pb2.DeleteBucketResponse.SerializeToString,
            ),
            'ListBuckets': grpc.unary_unary_rpc_method_handler(
                    servicer.ListBuckets,
                    request_deserializer=client__storage__pb2.ListBucketsRequest.FromString,
                    response_serializer=client__storage__pb2.ListBucketsResponse.SerializeToString,
            ),
            'HeadBucket': grpc.unary_unary_rpc_method_handler(
                    servicer.HeadBucket,
                    request_deserializer=client__storage__pb2.HeadBucketRequest.FromString,
                    response_serializer=client__storage__pb2.HeadBucketResponse.SerializeToString,
            ),
            'PutObject': grpc.stream_unary_rpc_method_handler(
                    servicer.PutObject,
                    request_deserializer=client__storage__pb2.PutObjectRequest.FromString,
                    response_serializer=client__storage__pb2.PutObjectResponse.SerializeToString,
            ),
            'GetObject': grpc.unary_stream_rpc_method_handler(
                    servicer.GetObject,
                    request_deserializer=client__storage__pb2.GetObjectRequest.FromString,
                    response_serializer=client__storage__pb2.GetObjectResponse.SerializeToString,
            ),
            'DeleteObject': grpc.unary_unary_rpc_method_handler(
                    servicer.DeleteObject,
                    request_deserializer=client__storage__pb2.DeleteObjectRequest.FromString,
                    response_serializer=client__storage__pb2.DeleteObjectResponse.SerializeToString,
            ),
            'DeleteObjects': grpc.unary_unary_rpc_method_handler(
                    servicer.DeleteObjects,
                    request_deserializer=client__storage__pb2.DeleteObjectsRequest.FromString,
                    response_serializer=client__storage__pb2.DeleteObjectsResponse.SerializeToString,
            ),
            'CopyObject': grpc.unary_unary_rpc_method_handler(
                    servicer.CopyObject,
                    request_deserializer=client__storage__pb2.CopyObjectRequest.FromString,
                    response_serializer=client__storage__pb2.CopyObjectResponse.SerializeToString,
            ),
            'HeadObject': grpc.unary_unary_rpc_method_handler(
                    servicer.HeadObject,
                    request_deserializer=client__storage__pb2.HeadObjectRequest.FromString,
                    response_serializer=client__storage__pb2.HeadObjectResponse.SerializeToString,
            ),
            'ListObjects': grpc.unary_stream_rpc_method_handler(
                    servicer.ListObjects,
                    request_deserializer=client__storage__pb2.ListObjectsRequest.FromString,
                    response_serializer=client__storage__pb2.ListObjectsResponse.SerializeToString,
            ),
            'Authenticate': grpc.unary_unary_rpc_method_handler(
                    servicer.Authenticate,
                    request_deserializer=client__storage__pb2.AuthRequest.FromString,
                    response_serializer=client__storage__pb2.AuthResponse.SerializeToString,
            ),
            'RotateKey': grpc.unary_unary_rpc_method_handler(
                    servicer.RotateKey,
                    request_deserializer=client__storage__pb2.RotateKeyRequest.FromString,
                    response_serializer=client__storage__pb2.RotateKeyResponse.SerializeToString,
            ),
            'ShareBucket': grpc.unary_unary_rpc_method_handler(
                    servicer.ShareBucket,
                    request_deserializer=client__storage__pb2.ShareBucketRequest.FromString,
                    response_serializer=client__storage__pb2.ShareBucketResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'proto.ObjectStorageCache', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('proto.ObjectStorageCache', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class ObjectStorageCache(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def CreateBucket(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/proto.ObjectStorageCache/CreateBucket',
            client__storage__pb2.CreateBucketRequest.SerializeToString,
            client__storage__pb2.CreateBucketResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def DeleteBucket(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/proto.ObjectStorageCache/DeleteBucket',
            client__storage__pb2.DeleteBucketRequest.SerializeToString,
            client__storage__pb2.DeleteBucketResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def ListBuckets(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/proto.ObjectStorageCache/ListBuckets',
            client__storage__pb2.ListBucketsRequest.SerializeToString,
            client__storage__pb2.ListBucketsResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def HeadBucket(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/proto.ObjectStorageCache/HeadBucket',
            client__storage__pb2.HeadBucketRequest.SerializeToString,
            client__storage__pb2.HeadBucketResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def PutObject(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_unary(
            request_iterator,
            target,
            '/proto.ObjectStorageCache/PutObject',
            client__storage__pb2.PutObjectRequest.SerializeToString,
            client__storage__pb2.PutObjectResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def GetObject(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(
            request,
            target,
            '/proto.ObjectStorageCache/GetObject',
            client__storage__pb2.GetObjectRequest.SerializeToString,
            client__storage__pb2.GetObjectResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def DeleteObject(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/proto.ObjectStorageCache/DeleteObject',
            client__storage__pb2.DeleteObjectRequest.SerializeToString,
            client__storage__pb2.DeleteObjectResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def DeleteObjects(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/proto.ObjectStorageCache/DeleteObjects',
            client__storage__pb2.DeleteObjectsRequest.SerializeToString,
            client__storage__pb2.DeleteObjectsResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def CopyObject(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/proto.ObjectStorageCache/CopyObject',
            client__storage__pb2.CopyObjectRequest.SerializeToString,
            client__storage__pb2.CopyObjectResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def HeadObject(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/proto.ObjectStorageCache/HeadObject',
            client__storage__pb2.HeadObjectRequest.SerializeToString,
            client__storage__pb2.HeadObjectResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def ListObjects(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(
            request,
            target,
            '/proto.ObjectStorageCache/ListObjects',
            client__storage__pb2.ListObjectsRequest.SerializeToString,
            client__storage__pb2.ListObjectsResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def Authenticate(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/proto.ObjectStorageCache/Authenticate',
            client__storage__pb2.AuthRequest.SerializeToString,
            client__storage__pb2.AuthResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def RotateKey(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/proto.ObjectStorageCache/RotateKey',
            client__storage__pb2.RotateKeyRequest.SerializeToString,
            client__storage__pb2.RotateKeyResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def ShareBucket(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/proto.ObjectStorageCache/ShareBucket',
            client__storage__pb2.ShareBucketRequest.SerializeToString,
            client__storage__pb2.ShareBucketResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
