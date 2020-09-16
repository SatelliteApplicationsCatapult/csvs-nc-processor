from typing import Dict, List, Generator
import requests
from src.config import LOG_FORMAT, LOG_LEVEL, tmp_dir, climate_data_url,\
    file_type, DateRange
import pathlib
import logging
from requests.exceptions import HTTPError

logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)
logger = logging.getLogger(__name__)


def get_input_occurrences(era5_url_structure: Dict[str, list]) -> List[str]:
    return list(era5_url_structure.keys())


def get_era5_url_suffixes(data_products: List[str], date_range: DateRange) -> List[str]:
    url_suffixes = []
    for product in data_products:
        for date in range(*date_range):
            url_suffixes.append(obtain_filename(product, str(date)))
    return url_suffixes


def download_era5_files(occurrence: str, url_suffixes: List[str]) -> Generator[str, None, None]:
    for product in url_suffixes:
        yield download_file(filename=product, data_type=occurrence)


def download_file(filename: str, data_type: str) -> str:
    file = create_tmp_file(filename)
    file_url = obtain_url_to_download(filename, data_type)

    try:
        logger.info(f'Downloading {file_url}...')
        response = requests.get(file_url)
        response.raise_for_status()
        with file.open('wb') as f:
            f.write(response.content)
    except HTTPError:
        logger.error(f'Error occurred trying to download {file_url}')
        raise

    return str(file)


def obtain_filename(data_name: str, data_year: str) -> str:
    return data_name + '_' + str(data_year) + file_type


def obtain_url_to_download(filename, data_type) -> str:
    return climate_data_url + data_type + '/' + filename


def create_tmp_file(filename: str) -> pathlib.Path:
    tmp_dir.mkdir(parents=True, exist_ok=True)
    return tmp_dir / filename


def create_output_file(input_file: str) -> str:
    return str(pathlib.Path(input_file).with_suffix('').with_suffix('.nc'))
