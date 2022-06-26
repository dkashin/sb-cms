from uuid import uuid4
from random import randint

import logging
logging.basicConfig(level=logging.DEBUG)

import requests

response = requests.post("http://localhost:11401/movies/4823/url", json=dict(
    login=149565,
    ip_address="79.173.88.34",
    user_agent="PyRequests",
    platform="json2",
    session_id=str(uuid4())
))

logging.info(response.text)

response = requests.post("http://localhost:11401/movies/files/5142/url", json=dict(
    login=149565,
    ip_address="79.173.88.34",
    user_agent="PyRequests",
    platform="json2",
    session_id=str(uuid4())
))

logging.info(response.text)