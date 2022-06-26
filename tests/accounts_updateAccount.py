import logging
logging.basicConfig(level=logging.DEBUG)

import requests

response = requests.get("http://localhost:11411/accounts/149565")
logging.debug(f"{response.status_code}: {response.text}")

response = requests.patch("http://localhost:11411/accounts/149565", json=dict(
    autocolo=False,
    live_colo=dict(name="deu")
))
logging.debug(f"{response.status_code}: {response.text}")

response = requests.get("http://localhost:11411/accounts/149565")
logging.debug(f"{response.status_code}: {response.text}")
