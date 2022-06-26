# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import channels_pb2 as channels__pb2


class ChannelsStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.getAvailableStreams = channel.unary_stream(
        '/stabox.Channels/getAvailableStreams',
        request_serializer=channels__pb2.Channel.SerializeToString,
        response_deserializer=channels__pb2.Stream.FromString,
        )
    self.getProgram = channel.unary_unary(
        '/stabox.Channels/getProgram',
        request_serializer=channels__pb2.Program.SerializeToString,
        response_deserializer=channels__pb2.Program.FromString,
        )
    self.findProgram = channel.unary_unary(
        '/stabox.Channels/findProgram',
        request_serializer=channels__pb2.Program.SerializeToString,
        response_deserializer=channels__pb2.Program.FromString,
        )


class ChannelsServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def getAvailableStreams(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def getProgram(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def findProgram(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_ChannelsServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'getAvailableStreams': grpc.unary_stream_rpc_method_handler(
          servicer.getAvailableStreams,
          request_deserializer=channels__pb2.Channel.FromString,
          response_serializer=channels__pb2.Stream.SerializeToString,
      ),
      'getProgram': grpc.unary_unary_rpc_method_handler(
          servicer.getProgram,
          request_deserializer=channels__pb2.Program.FromString,
          response_serializer=channels__pb2.Program.SerializeToString,
      ),
      'findProgram': grpc.unary_unary_rpc_method_handler(
          servicer.findProgram,
          request_deserializer=channels__pb2.Program.FromString,
          response_serializer=channels__pb2.Program.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'stabox.Channels', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))