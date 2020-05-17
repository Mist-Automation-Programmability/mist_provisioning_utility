import mist.api
from typing import AnyStr, Dict


class Sitegroup(object):

    """Mist Sitegroup Object"""

    name: str
    org_id: str
    api: mist.api.API
    sitegroup_id: str = None
    site_ids: [str] = None

    def __init__(self, name: str, org_id: str, api: mist.api.API, sitegroup_id: str = None, site_ids: [str] = None):
        self.name = name
        self.org_id = org_id
        self.api = api
        self.sitegroup_id = sitegroup_id
        self.site_ids = site_ids

    @property
    def settings(self) -> Dict:
        res = self.api.http_get__(f"orgs/{self.api.org_id}/sitegroups/{self.sitegroup_id}")
        return res.json()

    @property
    def to_mist(self) -> Dict:
        sg_data = {
            "id": self.sitegroup_id,
            "name": self.name,
            "org_id": self.org_id
        }
        if self.site_ids:
            sg_data['site_ids'] = self.site_ids
        return sg_data

    def __repr__(self) -> AnyStr:
        return str(self.to_mist)

    def __str__(self) -> AnyStr:
        s = f"<{self.__class__.__name__} object -  Name: '{self.name}', ID: '{self.sitegroup_id}'>"
        return s
