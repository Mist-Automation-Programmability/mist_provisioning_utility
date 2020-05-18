# Standard library imports
from typing import AnyStr, Dict, List, Optional  # https://docs.python.org/3/library/typing.html?highlight=typing#module-typing
import csv  # https://docs.python.org/3/library/csv.html?highlight=csv#module-csv
from pathlib import Path  # https://docs.python.org/3/library/pathlib.html?highlight=pathlib#module-pathlib
import time
# External imports
import geocoder
import requests
# Module imports
from src import logger  # Custom logging object


def parse_csv_file(csv_file: AnyStr) -> List[Dict]:
    csv_path = Path(csv_file).expanduser().absolute()
    csv_data = list()
    with csv_path.open('r') as csv_stream:
        data = csv.DictReader(csv_stream)
        for row in data:
            for k, v in row.items():
                if len(row[k]) == 0:
                    row[k] = None
            csv_data.append(row)
    return csv_data


def find_mist_object_id_by_name(name: AnyStr, objects: List) -> Optional[AnyStr]:
    name = name.strip()
    objects = [m.to_mist for m in objects]
    try:
        match = next(o for o in objects if o['name'] == name)
    except Exception as e:
        logger.error(f"Could not match object named '{name}' with anything in the list of objects provided.")
        logger.error(f"Exception: {e}")
        return None
    if match:
        return match['id']
    else:
        return None


def get_geo_info(address: str, api_key: str) -> (geocoder.google, dict):
    try:
        gaddr = geocoder.google(address, key=api_key)
    except Exception:
        raise
    tz_url = f"https://maps.googleapis.com/maps/api/timezone/json?location={gaddr.lat},{gaddr.lng}&timestamp={int(time.time())}&key={api_key}"
    try:
        tz_res = requests.get(url=tz_url)
    except Exception:
        raise
    tz_data = tz_res.json()
    return gaddr, tz_data
