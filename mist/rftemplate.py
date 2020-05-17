import mist.api
from typing import AnyStr, Dict


class RFTemplate(object):

    """Mist RF Template Object"""

    name: str
    api: mist.api.API
    rftemplate_id: str = None
    org_id: str = None

    def __init__(self, name: str, api: mist.api.API, rftemplate_id: str = None, org_id: str = None, **kwargs):
        self.name = name
        self.api = api
        self.rftemplate_id = rftemplate_id
        self.org_id = org_id
        for k, v in kwargs.items():
            setattr(self, k, v)

    @property
    def settings(self) -> Dict:
        res = self.api.http_get__(f"orgs/{self.api.org_id}/rftemplates/{self.rftemplate_id}")
        return res.json()

    @property
    def to_mist(self) -> Dict:
        rft_data = {
            "id": self.rftemplate_id,
            "name": self.name,
            "org_id": self.org_id,
            "ant_gain_5": self.__dict__.get('ant_gain_5', 0),
            "ant_gain_24": self.__dict__.get('ant_gain_24', 0),
            "model_specific": self.__dict__.get('model_specific', {}),
            "band_5": self.__dict__.get('band_5'),
            "band_24": self.__dict__.get('band_24')
        }
        if 'country_code' in self.__dict__ and len(self.__dict__['country_code']) == 2:
            rft_data['country_code'] = self.__dict__['country_code']
        return rft_data

    def __repr__(self) -> AnyStr:
        return str(self.to_mist)

    def __str__(self) -> AnyStr:
        s = f"<{self.__class__.__name__} object -  Name: '{self.name}', ID: '{self.rftemplate_id}'>"
        return s
