import requests
from config import LOG_FORMAT, LOG_LEVEL, tmp_dir, data_url, data, \
    data_interval, file_type
import pathlib
import logging

logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)
logger = logging.getLogger(__name__)


def obtain_files():
    for t in data:
        for d in data[t]:
            for y in data_interval:
                filename = d + '_' + str(y) + file_type
                file = download_file(filename, t)
                output_nc_file = pathlib.Path(file.name.split('.')[0] + '.nc')
                yield file, output_nc_file


def download_file(filename, t):
    file = tmp_dir / filename
    file_url = data_url + t + '/' + filename
    tmp_dir.mkdir(parents=True, exist_ok=True)

    logger.info(f'Downloading {file_url}...')
    r = requests.get(file_url)

    if r.ok:
        with file.open('wb') as f:
            f.write(r.content)
    else:
        logger.warning(f'Could not download {file_url}...')

    return file
