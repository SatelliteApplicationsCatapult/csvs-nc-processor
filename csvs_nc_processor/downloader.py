import requests
from config import LOG_FORMAT, LOG_LEVEL, tmp_dir, climate_data_url, \
    climate_data_to_download, climate_data_interval, file_type
import pathlib
import logging

logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)
logger = logging.getLogger(__name__)


def obtain_input_output_files() -> [pathlib.Path, pathlib.Path]:
    for t in climate_data_to_download:
        for d in climate_data_to_download[t]:
            for y in climate_data_interval:
                filename = obtain_filename(d, y)
                yield download_file(filename, t), create_output_file(filename)


def download_file(filename: str, data_type: str) -> pathlib.Path:
    file = create_tmp_file(filename)
    file_url = obtain_url_to_download(filename, data_type)

    logger.info(f'Downloading {file_url}...')
    r = requests.get(file_url)

    if r.ok:
        with file.open('wb') as f:
            f.write(r.content)
    else:
        logger.warning(f'Could not download {file_url}...')

    return file


def obtain_filename(data_name: str, data_year: str) -> str:
    return data_name + '_' + str(data_year) + file_type


def obtain_url_to_download(filename, data_type) -> str:
    return climate_data_url + data_type + '/' + filename


def create_tmp_file(filename: str) -> pathlib.Path:
    tmp_dir.mkdir(parents=True, exist_ok=True)
    return tmp_dir / filename


def create_output_file(filename: str) -> pathlib.Path:
    output_name = filename.split('.')[0] + '.nc'
    return tmp_dir / output_name
