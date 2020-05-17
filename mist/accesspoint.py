import mist.api
from typing import Dict, List, Optional, Union
from mist import logger


class AccessPoint(object):
    """Mist Access Point Object"""

    hostname: str
    serial: str
    org_id: str
    api: mist.api.API
    name: str = None
    site_id: str = None
    mac: str = None

    def __init__(self, hostname: str, serial: str, org_id: str, api: mist.api.API, **kwargs):
        self.hostname = hostname
        self.serial = serial
        self.org_id = org_id
        self.api = api
        for k, v in kwargs.items():
            setattr(self, k, v)
        if self.name and self.site_id and self.mac and (self.hostname != self.name):
            self.rename(self.hostname)

    def claim_to_org(self, claim_code: str = None):
        if claim_code:
            magic = claim_code
        elif hasattr(self, 'magic'):
            magic = self.magic
        elif hasattr(self, 'claim_code'):
            magic = self.claim_code
        else:
            raise ValueError("No claim code provided.")
        logger.debug(f"Claim code for {self.hostname} - {self.mac}: {magic}")
        url = f"orgs/{self.org_id}/inventory"
        payload = [magic]
        res = self.api.http_post__(url=url, body=payload)
        if res.status_code != 200:
            logger.error(f"Could not claim device {self.serial}")
            logger.error(f"Response: {res.content}")
            return False
        data = res.json()
        if magic.upper() in data['added']:
            logger.info(f"Checking device details from response...")
            for device in data['inventory_added']:
                if device['mac'] == self.mac:
                    logger.debug("Updating device attributes...")
                    for k, v in device.items():
                        setattr(self, k, v)
                    return True
        else:
            return False

    def unclaim(self):
        url = f"orgs/{self.org_id}/inventory"
        payload = {
            "op": "delete",
            "serials": [self.serial],
            "macs": [self.mac]
        }
        res = self.api.http_put__(url=url, body=payload)
        data = res.json()
        if self.serial in data['success']:
            return True
        else:
            return False

    def rename(self, name: str):
        if not self.name:
            logger.debug(f"Renaming {self.mac} to {name}...")
        else:
            logger.debug(f"Renaming {self.name} to {name}...")
        if self.site_id and self.mac:
            url = f"sites/{self.site_id}/devices/{self.device_id}"
            payload = {"name": name}
            res = self.api.http_put__(url=url, body=payload)
            if res.status_code == 200:
                self.hostname = self.name = name
                return True
            else:
                return res.json()
        else:
            logger.warning(f"Could not rename device {self.hostname} to {name}. "
                           "Device must have a site ID or MAC address assigned.")
            return False

    def update_from_org_inventory(self) -> bool:
        url = f"orgs/{self.org_id}/inventory?serial={self.serial}"
        try:
            res = self.api.http_get__(url=url)
            if res.status_code != 200:
                raise ConnectionError(f"Connection error {self.serial}: {res.content}")
        except Exception as e:
            logger.error(f"Could not update device {self.hostname} from org inventory.")
            logger.error(f"Error: {e}")
            return False
        data = res.json()
        if len(data) == 0:
            return False
        for k, v in data[0].items():
            setattr(self, k, v)
        return True

    def assign_to_site(self, site_id: str, no_reassign: bool = False) -> (bool, Optional[Union[Dict, List]]):
        status = False
        self.site_id = site_id
        url = f"orgs/{self.org_id}/inventory"
        payload = {
            "op": "assign",
            "site_id": self.site_id,
            "macs": [self.mac],
            "no_reassign": no_reassign
        }
        res = self.api.http_put__(url=url, body=payload)
        res_data = res.json()
        if res.status_code == 200:
            if self.mac in res_data['success']:
                status = True
            else:
                status = False
        return status, res_data

    @property
    def device_id(self):
        if hasattr(self, 'mac') and self.mac:
            return f"00000000-0000-0000-1000-{self.mac.lower()}"
        else:
            return None
