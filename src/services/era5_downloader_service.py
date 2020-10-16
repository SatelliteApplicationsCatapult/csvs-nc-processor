import sys
from typing import List, Generator
import requests
from load_config import LOG_FORMAT, LOG_LEVEL, tmp_dir
import pathlib
import logging
from requests.exceptions import HTTPError
from utils import make_url


logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)
logger = logging.getLogger(__name__)


def download_products(products: List[str]) -> Generator[str, None, None]:
    for product in products:
        yield download_file(url=product)


def download_file(url: str) -> str:
    filename = url.split('/')[-1]
    file = create_tmp_file(filename)

    try:
        logger.info(f'Downloading {url}...')
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with file.open('wb') as f:
            dl = 0
            total_length = int(response.headers.get('content-length'))
            for data in response.iter_content(chunk_size=4096):
                dl += len(data)
                f.write(data)
                done = int(50 * dl / total_length)
                sys.stdout.write(f"\r[{'=' * done}{' ' * (50 - done)}] {dl}/{total_length}B ({done * 2}%)")
                sys.stdout.flush()
            sys.stdout.write("\n")
    except HTTPError:
        logger.error(f'Error occurred trying to download {url}')
        raise

    return str(file)


def create_tmp_file(filename: str) -> pathlib.Path:
    tmp_dir.mkdir(parents=True, exist_ok=True)
    return tmp_dir / filename



