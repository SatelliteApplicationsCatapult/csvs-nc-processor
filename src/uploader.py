import boto3
from botocore.exceptions import ClientError
from src.config import LOG_FORMAT, LOG_LEVEL, \
    s3_id, s3_url, s3_key, s3_bucket
import logging
import pathlib
import os
import sys
import threading

logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)
logger = logging.getLogger(__name__)


def upload_to_s3(filepath: str) -> None:
    try:
        logger.info(f"Uploading {filepath} to {s3_bucket} bucket...")
        s3_client = boto3.client('s3', endpoint_url=s3_url, aws_access_key_id=s3_id,
                                 aws_secret_access_key=s3_key)
        s3_client.upload_file(filepath, s3_bucket, pathlib.Path(filepath).name,
                              Callback=ProgressPercentage(filepath))
    except Exception as e:
        raise UploadError(e)


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