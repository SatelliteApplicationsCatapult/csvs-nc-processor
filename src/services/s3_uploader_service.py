import boto3
from src.load_config import LOG_FORMAT, LOG_LEVEL, get_aws_config

import logging
import pathlib
import os
import sys
import threading

logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)
logger = logging.getLogger(__name__)


def upload_to_s3(filepath: str) -> None:
    try:
        s3_url, s3_id, s3_key, s3_bucket = get_aws_config()
        logger.info(f"Uploading {filepath} to {s3_bucket} bucket...")
        s3_client = boto3.client('s3', endpoint_url=s3_url, aws_access_key_id=s3_id,
                                 aws_secret_access_key=s3_key)
        file = pathlib.Path(filepath)
        dataset = file.stem.split('_')[0]

        s3_path = f"{dataset}/{file.name}"
        my_registry = {
            'daily': generate_s3_path_era5_daily,
            'monthly': generate_s3_path_era5,
            '30year': generate_s3_path_era5
        }
        for k, v in my_registry.items():
            if k in filepath:
                s3_path = v(dataset, k, filepath)

        s3_client.upload_file(filepath, s3_bucket, s3_path,
                              Callback=ProgressPercentage(filepath))
    except Exception as e:
        raise UploadError(e)


def generate_s3_path_era5(dataset: str, occurrence: str, filepath: str) -> str:
    file = pathlib.Path(filepath)
    return f"{dataset}/{occurrence}/{file.name}"


def generate_s3_path_era5_daily(dataset: str, occurrence: str, filepath: str) -> str:
    file = pathlib.Path(filepath)
    return f"{dataset}/{occurrence}/{file.stem[:-5]}/{file.name}"


class ProgressPercentage(object):

    def __init__(self, filename):
        self._filename = filename
        self._size = float(os.path.getsize(filename))
        self._seen_so_far = 0
        self._lock = threading.Lock()

    def __call__(self, bytes_amount):
        # To simplify, assume this is hooked up to a single filename
        with self._lock:
            self._seen_so_far += bytes_amount
            percentage = (self._seen_so_far / self._size) * 100
            sys.stdout.write(
                "\r%s  %s / %s  (%.2f%%)" % (
                    self._filename, self._seen_so_far, self._size,
                    percentage))
            sys.stdout.flush()


class UploadError(Exception):
    """Base class for exceptions in this module."""
    pass

if __name__ == '__main__':
    upload_to_s3('tests/resources/ERA5-Land_monthly_mean_2mTemp_1981_2019.nc')
