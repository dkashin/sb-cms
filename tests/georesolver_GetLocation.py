import os
import sys
sys.path.append(os.path.abspath("../common"))

import grpc
import georesolver_pb2, georesolver_pb2_grpc

import logging
logging.basicConfig(level=logging.INFO)

channel = grpc.insecure_channel(os.environ.get("ROUTER_ADDRESS"))
GeoResolver = georesolver_pb2_grpc.GeoResolverStub(channel)

def print_location(ip_address):
    try:
        rep = GeoResolver.GetLocation(
            georesolver_pb2.GetLocationReq(
                ip_address=ip_address
            )
        )
        logging.info("{}: {}".format(ip_address, rep))
    except grpc.RpcError as e:
        logging.error("Server responds with %s" % e.code())

for ip in ["113.228.6.109", "23.111.81.228", "37.208.104.202", "93.189.147.146", "79.173.88.34"]:
    print_location(ip)
