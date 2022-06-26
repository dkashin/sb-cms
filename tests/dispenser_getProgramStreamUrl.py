import os
import sys
sys.path.append(os.path.abspath("../common"))

import time
import logging
logging.basicConfig(level=logging.DEBUG)

from random import randint

import requests
import grpc
import dispenser_pb2, dispenser_pb2_grpc

channel = grpc.insecure_channel(os.environ.get("ROUTER_ADDRESS"))
Dispenser = dispenser_pb2_grpc.DispenserStub(channel)

for platform in "json json2".split():
    for force_hls in [True, False]:
        # response = make_grpc_call(platform, force_hls)
        try:
            reply = Dispenser.getProgramStreamUrl(
                dispenser_pb2.StreamUrlReq(
                    login=149565,
                    ip_address="79.173.88.34",
                    user_agent="PyGrpc",
                    content_id=1564065143,
                    platform=platform,
                    force_hls=force_hls
                )
            )
            logging.info(reply)
        except grpc.RpcError as e:
            logging.error("Server responds with %s" % e.code())

logging.info("Now via REST gateway:")

response = requests.post("http://localhost:11411/programs/481/requests", json=dict(
    login=149565,
    ip_address="79.173.88.34",
    user_agent="PyRequests",
    platform="json2",
    time_start=int(time.time() - 86400),
    force_hls=True
))

logging.debug(response.status_code)
logging.debug(response.text)
