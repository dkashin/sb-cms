import os
import sys
sys.path.append(os.path.abspath("../common"))

import grpc
import services_pb2, services_pb2_grpc
from random import randint

import logging
logging.basicConfig(level=logging.INFO)

channel = grpc.insecure_channel(os.environ.get("ROUTER_ADDRESS"))
Services = services_pb2_grpc.ServicesStub(channel)

def make_a_call():
    try:
        for colo in Services.getColos(services_pb2.Nothing()).items:
            logging.info(colo)
    except grpc.RpcError as e:
        logging.error("Server responds with %s" % e.code())

make_a_call()
