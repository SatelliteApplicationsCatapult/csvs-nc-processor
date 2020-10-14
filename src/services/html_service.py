import logging
from os import path
from typing import List, Optional

import requests
from bs4 import BeautifulSoup
from requests.exceptions import HTTPError

from load_config import LOG_LEVEL, LOG_FORMAT

logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)
logger = logging.getLogger(__name__)


def get_html_data_list(site: str) -> List[str]:
    result = []
    html = requests.get(site)
    try:
        html.raise_for_status()
    except HTTPError as err:
        logger.error(f'cannot get html from {site} because of {html.status_code}')
    soup = BeautifulSoup(html.text, 'html.parser')
    for link in soup.find_all('a'):
        if link.get('href').startswith('ERA5'):
            result.append(link.get('href'))
    return result


def download_file(site: str, dest_path: str) -> Optional[str]:
    with requests.get(site, stream=True) as r:
        try:
            r.raise_for_status()
        except HTTPError as err:
            print(
                f'cannot download file from {site} because of {r.status_code}')
        try:
            if path.exists(dest_path):
                print(f'file {dest_path} already downloaded')
                return dest_path
            with open(dest_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        except Exception as e:
            print(f'cannot download file because of {e}')
            dest_path = None
    return dest_path
