# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import Server_pb2 as Server__pb2


class ClientWriteServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.ClientWrite = channel.unary_unary(
                '/Server.ClientWriteService/ClientWrite',
                request_serializer=Server__pb2.ClientWriteRequest.SerializeToString,
                response_deserializer=Server__pb2.ClientWriteResponse.FromString,
                )


class ClientWriteServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def ClientWrite(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ClientWriteServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'ClientWrite': grpc.unary_unary_rpc_method_handler(
                    servicer.ClientWrite,
                    request_deserializer=Server__pb2.ClientWriteRequest.FromString,
                    response_serializer=Server__pb2.ClientWriteResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'Server.ClientWriteService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class ClientWriteService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def ClientWrite(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Server.ClientWriteService/ClientWrite',
            Server__pb2.ClientWriteRequest.SerializeToString,
            Server__pb2.ClientWriteResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)


class ClientReadServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.ClientRead = channel.unary_unary(
                '/Server.ClientReadService/ClientRead',
                request_serializer=Server__pb2.ClientReadRequest.SerializeToString,
                response_deserializer=Server__pb2.ClientReadResponse.FromString,
                )


class ClientReadServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def ClientRead(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ClientReadServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'ClientRead': grpc.unary_unary_rpc_method_handler(
                    servicer.ClientRead,
                    request_deserializer=Server__pb2.ClientReadRequest.FromString,
                    response_serializer=Server__pb2.ClientReadResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'Server.ClientReadService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class ClientReadService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def ClientRead(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Server.ClientReadService/ClientRead',
            Server__pb2.ClientReadRequest.SerializeToString,
            Server__pb2.ClientReadResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)


class ClientDeleteServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.ClientDelete = channel.unary_unary(
                '/Server.ClientDeleteService/ClientDelete',
                request_serializer=Server__pb2.ClientDeleteRequest.SerializeToString,
                response_deserializer=Server__pb2.ClientDeleteResponse.FromString,
                )


class ClientDeleteServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def ClientDelete(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ClientDeleteServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'ClientDelete': grpc.unary_unary_rpc_method_handler(
                    servicer.ClientDelete,
                    request_deserializer=Server__pb2.ClientDeleteRequest.FromString,
                    response_serializer=Server__pb2.ClientDeleteResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'Server.ClientDeleteService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class ClientDeleteService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def ClientDelete(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Server.ClientDeleteService/ClientDelete',
            Server__pb2.ClientDeleteRequest.SerializeToString,
            Server__pb2.ClientDeleteResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
