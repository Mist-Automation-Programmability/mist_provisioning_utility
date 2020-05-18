from typing import Dict, List, Union
from enum import Enum
import requests
import json
from mist import logger
from src.config import Config


class MistCloud(Enum):

    STD = "https://api.mist.com/api/v1/{}"
    EU = "https://api.eu.mist.com/api/v1/{}"


class API(object):

    """Mist API Object"""

    base_url: str
    api_token: str = None
    org_id: str = None
    cache_timeout: int = 10
    overwrite_devices: bool = False
    google_api_token: str = None

    def __init__(self, config: Config, cloud: MistCloud = MistCloud.STD):
        logger.debug("Initializing Mist API object...")
        self.base_url = cloud.value
        self.api_token = config.mist.api_token
        self.org_id = config.mist.org_id
        self.cache_timeout = config.mist.cache_timeout
        self.overwrite_devices = config.mist.overwrite_device
        self.google_api_token = config.google.api_token
        if not self.verify():
            logger.error("Unable to connect to the Mist API.")
            raise ValueError("Unable to connect to Mist API.")

    def verify(self) -> bool:
        try:
            res = self.http_get__()
            if res.status_code == 200:
                return True
            else:
                raise ValueError(f"Unable to connect to Mist API, response is '{res.status_code} - {res.content}'")
        except Exception:
            raise

    def http_get__(self, url: str = "self") -> requests.Response:
        url = self.base_url.format(url)
        try:
            res = requests.get(url=url, headers=self.headers)
        except Exception:
            raise
        return res

    def http_post__(self, url: str, body: Union[Dict, List]) -> requests.Response:
        url = self.base_url.format(url)
        try:
            res = requests.post(url=url, data=json.dumps(body), headers=self.headers)
        except Exception:
            raise
        return res

    def http_put__(self, url: str, body: Union[Dict, List]) -> requests.Response:
        url = self.base_url.format(url)
        try:
            res = requests.put(url=url, data=json.dumps(body), headers=self.headers)
        except Exception:
            raise
        return res

    def http_delete__(self, url: str) -> requests.Response:
        url = self.base_url.format(url)
        try:
            res = requests.delete(url=url, headers=self.headers)
        except Exception:
            raise
        return res

    @property
    def headers(self):
        h = {
            "Content-type": "application/json",
            "Authorization": f"Token {self.api_token}"
        }
        return h
