import os
import sys
sys.path.append(os.path.abspath("../common"))

from uuid import uuid4

import logging
logging.basicConfig(level=logging.DEBUG)
logging.getLogger("requests").setLevel(logging.WARNING)

from random import randint

import grpc
import dispenser_pb2, dispenser_pb2_grpc
import requests

# channel = grpc.insecure_channel(os.environ.get("ROUTER_ADDRESS", "localhost:11410"))
# Dispenser = dispenser_pb2_grpc.DispenserStub(channel)

# try:
#     reply = Dispenser.getChannelStreamUrl(
#         dispenser_pb2.StreamUrlReq(
#             login=149565,
#             ip_address="79.173.88.34",
#             user_agent="PyGrpc",
#             content_id=481,
#             platform="json2",
#             session_id=str(uuid4())
#         )
#     )
#     logging.info(reply)
# except grpc.RpcError as e:
#     logging.error("Server responds with %s" % e.code())

def make_req(session_id=None):
    if not session_id:
        session_id = str(uuid4())
    # response = requests.post("http://localhost:11411/channels/481/requests", json=dict(
    response = requests.post("http://beta.stabox.newru.tv/api/v1/channels/481/requests", json=dict(
        login=149565,
        ip_address="79.173.88.34",
        user_agent="PyRequests",
        platform="json2",
        session_id=session_id
    ))
    try:
        logging.debug(f"Using session {session_id}")
        url = f"http://{response.json()['stream_url']}"
        logging.info(f"\n\ncvlc --width=320 --height=240 '{url}'\n\n")
    except:
        logging.info(response.text)
    return session_id

session_id0 = make_req()
# session_id1 = make_req()
# session_id2 = make_req()
# session_id1 = make_req(session_id1)
# session_id2 = make_req(session_id2)
# session_id1 = make_req(session_id1)
# session_id1 = make_req(session_id1)
