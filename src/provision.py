# Standard library imports
from typing import List  # https://docs.python.org/3/library/typing.html?highlight=typing#module-typing
from pathlib import Path  # https://docs.python.org/3/library/pathlib.html?highlight=pathlib#module-pathlib
# Internal imports
from mist import Mist  # Mist object
from mist.site import Site  # Mist Site object
from mist.accesspoint import AccessPoint  # Mist Access Point object
from src import logger  # Custom logging object


def provision_sites(csv_file: Path, mist: Mist) -> List[Site]:
    logger.info(f"Creating sites from csv file {csv_file.name}...")
    new_sites, created = mist.org.create_sites(csv_file=csv_file)
    logger.info(f"Provisioned {created} sites.")
    return new_sites


def provision_devices(csv_file: Path, mist: Mist) -> List[AccessPoint]:
    logger.info(f"Creating devices and assigning to sites from csv file {csv_file.name}...")
    new_devices, assigned = mist.org.assign_devices_from_csv(csv_file=csv_file)
    logger.info(f"Claimed and/or assigned {assigned} devices.")
    return new_devices
