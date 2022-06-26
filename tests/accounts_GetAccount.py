import os
import sys
sys.path.append(os.path.abspath("../common"))

import grpc
import accounts_pb2, accounts_pb2_grpc
from random import randint

import logging
logging.basicConfig(level=logging.INFO)

channel = grpc.insecure_channel(str(os.environ.get("ROUTER_ADDRESS")))
Accounts = accounts_pb2_grpc.AccountsStub(channel)

try:
    rep = Accounts.GetAccount(
        accounts_pb2.Account(
            login=221082
        )
    )
    logging.info(rep)
except grpc.RpcError as e:
    logging.error("Server responds with %s" % e.code())
