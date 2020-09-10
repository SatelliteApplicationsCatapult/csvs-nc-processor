import boto3
from botocore.exceptions import ClientError
from utils import path_to_str
from config import LOG_FORMAT, LOG_LEVEL, output_nc_file, \
    s3_id, s3_url, s3_key, s3_bucket
import logging
import pathlib

logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)
logger = logging.getLogger(__name__)


def upload_to_s3(filepath: pathlib.Path):
    logger.info(f"Uploading {filepath} to {s3_bucket} bucket...")
    s3_client = boto3.client('s3', endpoint_url=s3_url, aws_access_key_id=s3_id,
                             aws_secret_access_key=s3_key)
    try:
        s3_client.upload_file(path_to_str(filepath), s3_bucket, filepath.name)
    except ClientError as e:
        logger.error(e)
    finally:
        output_nc_file.unlink()
