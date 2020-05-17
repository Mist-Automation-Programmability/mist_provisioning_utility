import mist.api
from src.utils import get_geo_info
from src import logger


class Site(object):

    """Mist Site Object"""

    name: str
    api: mist.api.API
    site_id: str
    org_id: str = None
    lat: float = None
    lng: float = None
    timezone: str = None
    country_code: str = None
    sitegroup_ids: [str] = None
    __address: str = None

    def __init__(self, name: str, api: mist.api.API, site_id: str = None, org_id: str = None, **kwargs):
        self.name = name
        self.api = api
        self.site_id = site_id
        self.org_id = org_id
        for k, v in kwargs.items():
            if k == 'address':
                self.__address = v
            elif k == 'latlng':
                self.lat = v.get('lat')
                self.lng = v.get('lng')
            else:
                setattr(self, k, v)
        if self.__address:
            logger.debug(f"Getting location information for site: {self.name}")
            self.__update_location__(address=self.__address)
            logger.debug(f"Location information updated for site: {self.name}")
        logger.debug(f"Finished building site: {self.name}")

    # TODO: write function to save changes
    # def update(self) -> bool:
    #     try:
    #         res = self.api.http_put__(url=f"sites/{self.site_id}/s")

    def create(self) -> (bool, dict):
        try:
            res = self.api.http_post__(url=f"orgs/{self.org_id}/sites", body=self.to_mist)
        except Exception:
            raise
        res_data = res.json()
        if res.status_code == 200:
            self.site_id = res_data['id']
            status = True
        else:
            status = False
        return status, res_data

    def delete(self) -> (bool, dict):
        try:
            res = self.api.http_delete__(url=f"sites/{self.site_id}")
        except Exception:
            raise
        res_data = res.json()
        if res.status_code == 200:
            status = True
        else:
            status = False
        return status, res_data

    def __update_location__(self, address: str):
        addr_data, tz_data = get_geo_info(address=address, api_key=self.api.google_api_token)
        try:
            self.country_code = addr_data.country
            self.timezone = tz_data.get('timeZoneId')
            self.__address = addr_data.address
            self.lat = addr_data.lat
            self.lng = addr_data.lng
        except Exception:
            raise

    @property
    def address(self) -> str:
        return self.__address

    @address.setter
    def address(self, new_address: str):
        self.__update_location__(address=new_address)

    @property
    def latlng(self) -> dict:
        latlng = {
            "lat": self.lat,
            "lng": self.lng
        }
        return latlng

    @latlng.setter
    def latlng(self, new_latlng: dict):
        self.lat = new_latlng.get('lat')
        self.lng = new_latlng.get('lng')

    @property
    def settings(self) -> dict:
        res = self.api.http_get__(f"sites/{self.site_id}/setting")
        return res.json()

    @property
    def to_mist(self) -> dict:
        site_data = {
            "name": self.name,
            "org_id": self.org_id,
            "country_code": self.country_code,
            "timezone": self.timezone,
            "address": self.address,
            "sitegroup_ids": self.sitegroup_ids,
            "latlng": {
                "lat": self.lat,
                "lng": self.lng
            },
            "auto_upgrade": {
                "enabled": True,
                "version": "beta",
                "time_of_day": "02:00",
                "custom_versions": {},
                "day_of_week": "sun"
            },
            "persist_config_on_device": True,
            "enable_channel_144": True,
            "rtsa": {
                "enabled": True,
                "track_asset": True,
                "app_waking": True
            },
            "led": {
                "enabled": True,
                "brightness": 255
            },
            "wifi": {
                "enabled": True,
                "locate_unconnected": True,
                "mesh_enabled": False,
                "detect_interference": True
            },
            "rogue": {
                "min_rssi": -80,
                "min_duration": 10,
                "enabled": True,
                "honeypot_enabled": False,
                "whitelisted_bssids": [],
                "whitelisted_ssids": []
            },
            "analytic": {
                "enabled": True
            }
        }
        if self.site_id:
            site_data['id'] = self.site_id
        if 'sitegroup_ids' in self.__dict__:
            site_data['sitegroup_ids'] = self.__dict__['sitegroup_ids']
        if 'rftemplate_id' in self.__dict__:
            site_data['rftemplate_id'] = self.__dict__['rftemplate_id']
        if 'secpolicy_id' in self.__dict__:
            site_data['secpolicy_id'] = self.__dict__['secpolicy_id']
        if 'alarmtemplate_id' in self.__dict__:
            site_data['alarmtemplate_id'] = self.__dict__['alarmtemplate_id']
        if 'networktemplate_id' in self.__dict__:
            site_data['networktemplate_id'] = self.__dict__['networktemplate_id']
        return site_data

    def __repr__(self):
        return str(self.to_mist)

    def __str__(self):
        s = f"<{self.__class__.__name__} object -  Name: '{self.name}', ID: '{self.site_id}'>"
        return s
