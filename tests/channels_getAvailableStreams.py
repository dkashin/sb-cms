import os
import sys
sys.path.append(os.path.abspath("../common"))

import grpc
import channels_pb2, channels_pb2_grpc
from random import randint

import logging
logging.basicConfig(level=logging.INFO)

channel = grpc.insecure_channel(os.environ.get("ROUTER_ADDRESS"))
Channels = channels_pb2_grpc.ChannelsStub(channel)

try:
    for stream in Channels.getAvailableStreams(channels_pb2.Channel(channel_id=481)):
        logging.info(stream)
except grpc.RpcError as e:
    logging.error("Server responds with %s" % e.code())
