import os
from logging import INFO
import pathlib

LOG_FORMAT = '%(asctime)s - %(name)12s - %(levelname)6s - %(message)s'
LOG_LEVEL = INFO

s3_url = os.getenv('S3_URL', 'url')
s3_bucket = os.getenv('S3_BUCKET', 'bucket')
s3_id = os.getenv('S3_ID', 'id')
s3_key = os.getenv('S3_KEY', 'key')

tmp_dir = pathlib.Path('./.tmp')
input_tar_file = pathlib.Path(os.getenv('INPUT_TAR_FILE', '../resources/ERA5_daily_mean_2mTemp_1980.tar.gz'))
output_nc_file = pathlib.Path(os.getenv('OUTPUT_NC_FILE', './' + input_tar_file.name.split('.')[0] + '.nc'))
std_name = os.getenv('STD_NAME', 'air_temperature')
