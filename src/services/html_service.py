import logging
from typing import List

import requests
from bs4 import BeautifulSoup
from requests.exceptions import HTTPError

from src.load_config import LOG_LEVEL, LOG_FORMAT

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
