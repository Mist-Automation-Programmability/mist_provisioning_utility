# Standard library imports
from typing import AnyStr, Dict, List, Union  # https://docs.python.org/3/library/typing.html?highlight=typing#module-typing
from pathlib import Path  # https://docs.python.org/3/library/pathlib.html?highlight=pathlib#module-pathlib
from time import time  # https://docs.python.org/3/library/time.html?highlight=time#module-time
# Module imports
import mist.api
import mist.site
import mist.rftemplate
import mist.sitegroup
import mist.accesspoint
from mist import logger
from src.utils import find_mist_object_id_by_name, parse_csv_file


class Organization(object):

    """Mist Organization Object"""

    api: mist.api.API
    org_id: str = None
    name: str
    sites: [mist.site.Site] = None
    __last_sites_refresh: float = 0
    sitegroups: list = None
    __last_sitegroups_refresh: float = 0
    rftemplates: [mist.rftemplate.RFTemplate]
    __last_rftemplates_refresh: float = 0
    inventory: list = [mist.accesspoint.AccessPoint]
    __last_inventory_refresh: float = 0

    def __init__(self, name: str, api: mist.api.API, org_id: str = None, **kwargs):
        """
        Initialize the Mist Organization object.

        :param str name: Organization name
        :param mist.api.API api: Mist API object
        :param str org_id: Organization ID
        :param dict kwargs: Optional dictionary containing additional attributes to be assigned
        """
        logger.debug(f"Initializing Mist Organization object: \"{name}\"")
        self.name = name
        self.api = api
        self.org_id = org_id
        for k, v in kwargs.items():
            setattr(self, k, v)
        try:
            self.get_sites()
        except Exception as e:
            logger.error(f"Exception getting organization sites: {e}")
            raise e
        try:
            self.get_rftemplates()
        except Exception as e:
            logger.error(f"Exception getting organization RF templates: {e}")
            raise e
        try:
            self.get_sitegroups()
        except Exception as e:
            logger.error(f"Exception getting organization site groups: {e}")
            raise e

    def update(self):
        # TODO: write function to save changes
        pass

    def refresh_sites(self):
        """
        Force a refresh of all sites in the organization

        :returns None
        """
        self.__last_sites_refresh = 0
        _ = self.get_sites()

    def get_sites(self) -> List[mist.site.Site]:
        """
        Retrieve a list of all the sites in the organization

        :returns List[mist.site.Site: A list of Mist Site objects.
        """
        now = time()
        if self.__last_sites_refresh > 0 and (now - self.__last_sites_refresh) < self.api.cache_timeout:
            pass
        else:
            res = self.api.http_get__(f"orgs/{self.org_id}/sites")
            self.__last_sites_refresh = time()
            site_list = res.json()
            sites = list()
            for site_data in site_list:
                site_id = site_data.pop('id')
                name = site_data.pop('name')
                site = mist.site.Site(name=name, api=self.api, site_id=site_id, **site_data)
                sites.append(site)
            self.sites = sites
        return self.sites

    def get_sitegroups(self) -> List[mist.sitegroup.Sitegroup]:
        """
        Retrieve all Sitegroups

        :return List[mist.sitegroup.Sitegroup: A list of Sitegroups in the organization
        """
        now = time()
        if self.__last_sitegroups_refresh > 0 and (now - self.__last_sitegroups_refresh) < self.api.cache_timeout:
            pass
        else:
            res = self.api.http_get__(f"orgs/{self.org_id}/sitegroups")
            self.__last_sitegroups_refresh = time()
            sitegroups_list = res.json()
            sitegroups = list()
            for sitegroup_data in sitegroups_list:
                sitegroup_id = sitegroup_data.pop('id')
                name = sitegroup_data.pop('name')
                org_id = sitegroup_data.pop('org_id')
                site_ids = sitegroup_data.pop('site_ids', None)
                sitegroup = mist.sitegroup.Sitegroup(name=name, org_id=org_id, api=self.api, sitegroup_id=sitegroup_id, site_ids=site_ids)
                sitegroups.append(sitegroup)
            self.sitegroups = sitegroups
        return self.sitegroups

    def get_rftemplates(self) -> List[mist.rftemplate.RFTemplate]:
        """
        Retrieve all RF Templates

        :return List[mist.rftemplate.RFTemplate: A list of RF Templates in the organization
        """
        now = time()
        if self.__last_rftemplates_refresh > 0 and (now - self.__last_rftemplates_refresh) < self.api.cache_timeout:
            pass
        else:
            res = self.api.http_get__(f"orgs/{self.org_id}/rftemplates")
            self.__last_rftemplates_refresh = time()
            rftemplate_list = res.json()
            rftemplates = list()
            for rftemplate_data in rftemplate_list:
                rftemplate_id = rftemplate_data.pop('id')
                name = rftemplate_data.pop('name')
                rftemplate = mist.rftemplate.RFTemplate(name=name, api=self.api, rftemplate_id=rftemplate_id,
                                                        **rftemplate_data)
                rftemplates.append(rftemplate)
            self.rftemplates = rftemplates
        return self.rftemplates

    # CSV based functions

    def create_sites(self, csv_file: Union[AnyStr, Path]) -> (List[mist.site.Site], int):
        """
        Create new sites from a CSV file

        :param Union[AnyStr, Path] csv_file: A string or pathlib.Path reference to the CSV file location
        :return List[mist.site.Site]: A list of created Mist sites
        """
        logger.debug("Starting site processing and building...")
        new_sites = self.build_sites(csv_file=csv_file)
        logger.debug(f"Starting site creation process for {len(new_sites)} sites...")
        created = 0
        for idx, new_site in enumerate(new_sites, start=1):
            logger.debug(f"Creating site #{idx}: {new_site.name}")
            status, response = new_site.create()
            if not status:
                logger.error(f"Failed to create site #{idx}: {new_site.name}")
            else:
                created += 1
                logger.info(f"Created site #{idx}: {new_site.name}")
        # Refresh sites from the Mist cloud before returning
        logger.debug("Verifying sites with Mist API...")
        self.refresh_sites()
        logger.debug("Completed site creation process.")
        return new_sites, created

    def build_sites(self, csv_file: Union[AnyStr, Path]) -> List[mist.site.Site]:
        """
        Construct new site objects from a CSV file

        :param Union[AnyStr, Path] csv_file: A string or pathlib.Path reference to the CSV file location
        :return List[mist.site.Site]: A list of Mist sites
        """
        logger.debug("Parsing CSV file...")
        sites_csv_data = parse_csv_file(csv_file=csv_file)
        new_sites = list()
        logger.debug(f"Processing {len(sites_csv_data)} sites...")
        for idx, site in enumerate(sites_csv_data, start=1):
            logger.debug(f"Processing site #{idx}: {site['name']}")
            if site['sitegroups']:
                sitegroups = site.pop('sitegroups').split(',')
                sitegroup_ids = list()
                for sitegroup in sitegroups:
                    sg_id = find_mist_object_id_by_name(sitegroup, self.sitegroups)
                    if sg_id:
                        sitegroup_ids.append(sg_id)
                    else:
                        site['sitegroup_ids'] = sitegroup_ids
            else:
                del site['sitegroups']
            if site['rftemplate']:
                site['rftemplate_id'] = find_mist_object_id_by_name(site['rftemplate'], self.rftemplates)
            else:
                del site['rftemplate']
            site['api'] = self.api
            site['org_id'] = self.org_id
            logger.debug(f"Building site #{idx}: {site['name']}")
            new_site = mist.site.Site(**site)
            new_sites.append(new_site)
        return new_sites

    def assign_devices_from_csv(self, csv_file: Union[AnyStr, Path]) -> (List[mist.accesspoint.AccessPoint], int):
        aps_csv_data = parse_csv_file(csv_file=csv_file)
        aps = list()
        assigned = 0
        for ap in aps_csv_data:
            try:
                new_ap = mist.accesspoint.AccessPoint(hostname=ap['hostname'], serial=ap['serial'], org_id=self.org_id, api=self.api, mac=ap['mac'])
            except Exception as e:
                logger.error(f"Exception occured creating new object: {e}")
                continue
            in_inventory = new_ap.update_from_org_inventory()
            if not in_inventory:
                if ap['claim_code']:
                    claimed = new_ap.claim_to_org(claim_code=ap['claim_code'])
                    if not claimed:
                        logger.error(f"Could not claim {new_ap.hostname} - {new_ap.serial} to org, skipping.")
                        continue
                    else:
                        logger.info(f"Claimed {new_ap.hostname} - {new_ap.serial} to org inventory.")
                else:
                    logger.error(f"No claim code provided for {new_ap.hostname} - {new_ap.serial}, skipping.")
                    continue
            else:
                if self.api.overwrite_devices:
                    logger.info(f"Device {new_ap.name} - {new_ap.serial} already in inventory, overwriting device configuration.")
                    logger.warning("Set the 'overwrite_devices' option to 'false' in your config file to prevent reassigning the device.")
                    pass
                else:
                    logger.error(f"Device {new_ap.name} - {new_ap.serial} already in inventory, skipping device configuration.")
                    logger.warning("Set the 'overwrite_devices' option to 'true' in your config file to reassign the device.")
                    continue
            try:
                logger.info(f"Attmepting to assign to site: {ap['site_name']}")
                site_id = find_mist_object_id_by_name(ap['site_name'], self.sites)
                if not site_id:
                    logger.error(f"Could not find site: {ap['site_name']}")
                    logger.error(f"Skipping device configuration...")
                    continue
                else:
                    new_ap.assign_to_site(site_id=site_id)
            except Exception as e:
                logger.error(f"Exception occurred assigning site: {e}")
                continue
            if ap['hostname'] != new_ap.name:
                new_ap.rename(ap['hostname'])
            else:
                logger.debug(f"Device name already up to date for {new_ap.hostname}")
            logger.debug(f"Finished privisioning device: {new_ap.hostname}")
            aps.append(new_ap)
            assigned += 1
        return aps, assigned

    # Computed properties

    @property
    def to_mist(self) -> Dict:
        org_data = {
            "name": self.name,
            "id": self.org_id,
            "msp_id": self.__dict__.get('msp_id', None),
            "allow_mist": self.__dict__.get('allow_mist', False),
            "session_expiry": self.__dict__.get('session_expiry', 1440),
            "alarmtemlpate_id": self.__dict__.get('alarmtemplate_id', None)
        }
        return org_data

    def __repr__(self):
        return str(self.to_mist)

    def __str__(self):
        return f"<{self.__class__.__name__} object -  Name: '{self.name}', ID: '{self.org_id}'>"
