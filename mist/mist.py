import mist.api
import mist.org
from time import time
from mist import logger
from src.config import Config


class Mist(object):

    """Mist Object"""

    api: mist.api.API
    org: mist.org.Organization = None
    orgs: [mist.org.Organization] = None
    __last_orgs_refresh: float = 0

    def __init__(self, config: Config):
        logger.debug("Initializing Mist object...")
        try:
            self.api = mist.api.API(config=config)
        except Exception as e:
            logger.debug(f"Exception creating Mist API object: {e}")
            raise e
        self.org = self.get_org()
        # TODO: Better handling of preloading orgs
        # self.get_orgs()

    def get_org(self, org_id: str = None) -> mist.org.Organization:
        logger.info("Loading organization from config file...")
        if not org_id:
            get_org_id = self.api.org_id
        else:
            get_org_id = org_id
        res = self.api.http_get__(f"orgs/{get_org_id}")
        org_data = res.json()
        org_id = org_data.pop('id')
        name = org_data.pop('name')
        org = mist.org.Organization(name=name, api=self.api, org_id=org_id, **org_data)
        return org

    def switch_org(self, org_id: str) -> mist.org.Organization:
        logger.info("Switching organization...")
        self.api.org_id = org_id
        self.org = self.get_org()
        return self.org

    def get_orgs(self) -> [mist.org.Organization]:
        logger.info("Loading all accessible organizations...")
        now = time()
        if self.__last_orgs_refresh > 0 and (now - self.__last_orgs_refresh) < self.api.cache_timeout:
            pass
        else:
            res = self.api.http_get__()
            self.__last_orgs_refresh = time()
            privs_list = res.json()['privileges']
            org_list = [o for o in privs_list if o['scope'] == 'org']
            orgs = list()
            for org_data in org_list:
                org_id = org_data.pop('org_id')
                name = org_data.pop('name')
                org = mist.org.Organization(name=name, api=self.api, org_id=org_id, **org_data)
                orgs.append(org)
            self.orgs = orgs
        return self.orgs
