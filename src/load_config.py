import os
from logging import INFO
from pathlib import Path
import json
from typing import Tuple

LOG_FORMAT = '%(asctime)s - %(name)12s - %(levelname)6s - %(message)s'
LOG_LEVEL = INFO

with open(Path(__file__).parent / "config.json") as json_data_file:
    config = json.load(json_data_file)

url = config['url']
datasets = config['datasets']
occurrences = config['occurrences']
start_value = config['start_value']
std_name = config['standard_names']
aoi = config['aoi']
units = config['units']

tmp_dir = Path.cwd() / '.tmp'


def get_aws_config() -> Tuple[str, str, str, str]:
    s3_url = os.getenv('S3_URL', 'http://s3-uk-1.sa-catapult.co.uk')
    s3_id = os.getenv('S3_ID', 'test_id')
    s3_key = os.getenv('S3_KEY', 'test_secret')
    s3_bucket = os.getenv('S3_BUCKET', 'csvs-netcdf')
    return s3_url, s3_id, s3_key, s3_bucket
