import time
import logging
logging.basicConfig(level=logging.DEBUG)

import requests

response = requests.post("http://localhost:11411/channels/481/requests", json=dict(
    login=149565,
    ip_address="78.194.234.239",
    user_agent="PyRequests",
    platform="json2"
))

logging.debug(response.status_code)
stream_url = response.json()["stream_url"]
logging.debug(stream_url)


response = requests.post("http://localhost:11411/colos/abuse", json=dict(
    stream_url=stream_url
))

logging.debug(response.status_code)
logging.debug(response.text)


response = requests.post("http://localhost:11411/colos/abuse", json=dict(
    stream_url=stream_url
))

logging.debug(response.status_code)
logging.debug(response.text)

response = requests.post("http://localhost:11411/channels/481/requests", json=dict(
    login=149565,
    ip_address="78.194.234.239",
    user_agent="PyRequests",
    platform="json2"
))

logging.debug(response.status_code)
stream_url = response.json()["stream_url"]
logging.debug(stream_url)