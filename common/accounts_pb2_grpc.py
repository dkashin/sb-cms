# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import accounts_pb2 as accounts__pb2


class AccountsStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.GetAccounts = channel.unary_unary(
        '/stabox.Accounts/GetAccounts',
        request_serializer=accounts__pb2.GetAccountsReq.SerializeToString,
        response_deserializer=accounts__pb2.GetAccountsRep.FromString,
        )
    self.GetAccount = channel.unary_unary(
        '/stabox.Accounts/GetAccount',
        request_serializer=accounts__pb2.Account.SerializeToString,
        response_deserializer=accounts__pb2.Account.FromString,
        )
    self.updateAccount = channel.unary_unary(
        '/stabox.Accounts/updateAccount',
        request_serializer=accounts__pb2.Account.SerializeToString,
        response_deserializer=accounts__pb2.Account.FromString,
        )
    self.SessionCreate = channel.unary_unary(
        '/stabox.Accounts/SessionCreate',
        request_serializer=accounts__pb2.SessionCreateReq.SerializeToString,
        response_deserializer=accounts__pb2.AccountSession.FromString,
        )


class AccountsServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def GetAccounts(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GetAccount(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def updateAccount(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def SessionCreate(self, request, context):
    """rpc updateAccounts(updateAccountsReq) returns (Account) {
    option (google.api.http) = {
    patch: "/accounts/{login}",
    body: "*"
    };
    }
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_AccountsServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'GetAccounts': grpc.unary_unary_rpc_method_handler(
          servicer.GetAccounts,
          request_deserializer=accounts__pb2.GetAccountsReq.FromString,
          response_serializer=accounts__pb2.GetAccountsRep.SerializeToString,
      ),
      'GetAccount': grpc.unary_unary_rpc_method_handler(
          servicer.GetAccount,
          request_deserializer=accounts__pb2.Account.FromString,
          response_serializer=accounts__pb2.Account.SerializeToString,
      ),
      'updateAccount': grpc.unary_unary_rpc_method_handler(
          servicer.updateAccount,
          request_deserializer=accounts__pb2.Account.FromString,
          response_serializer=accounts__pb2.Account.SerializeToString,
      ),
      'SessionCreate': grpc.unary_unary_rpc_method_handler(
          servicer.SessionCreate,
          request_deserializer=accounts__pb2.SessionCreateReq.FromString,
          response_serializer=accounts__pb2.AccountSession.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'stabox.Accounts', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
