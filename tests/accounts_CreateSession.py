import os
import sys
sys.path.append(os.path.abspath("../common"))

import grpc
import accounts_pb2, accounts_pb2_grpc
from random import randint

import logging
logging.basicConfig(level=logging.INFO)

channel = grpc.insecure_channel(os.environ.get("ROUTER_ADDRESS"))
Accounts = accounts_pb2_grpc.AccountsStub(channel)

def create_session(ip_address):
    try:
        rep = Accounts.SessionCreate(
            accounts_pb2.SessionCreateReq(
                login=149565,
                password="66252",
                ip_address=ip_address,
                user_agent="python",
            )
        )
        logging.info(rep)
    except grpc.RpcError as e:
        logging.error("Server responds with %s" % e.code())

for ip in ["113.228.6.109", "79.173.88.34"]:
    for _ in range(randint(2, 4)):
        create_session(ip)
