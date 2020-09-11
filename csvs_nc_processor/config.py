import os
from logging import INFO
import pathlib

LOG_FORMAT = '%(asctime)s - %(name)12s - %(levelname)6s - %(message)s'
LOG_LEVEL = INFO

s3_url = os.getenv('S3_URL', 'url')
s3_bucket = os.getenv('S3_BUCKET', 'bucket')
s3_id = os.getenv('S3_ID', 'id')
s3_key = os.getenv('S3_KEY', 'key')

tmp_dir = pathlib.Path.cwd() / '.tmp'
std_name = os.getenv('STD_NAME', 'air_temperature')

data_url = os.getenv('DATA_URL', 'http://37.128.186.209/LAURA/ERA5/')
data = {
    'daily': [
        'ERA5_daily_mean_2mTemp',
        'ERA5_daily_mean_RH',
        'ERA5_daily_mean_TotalWind',
        'ERA5_daily_mean_mslp',
        'ERA5_daily_mean_soil_temp_L1',
        'ERA5_daily_mean_soil_water_L1',
        'ERA5_daily_mean_sol_rad',
        'ERA5_daily_total_precipitation'
    ]
}
data_interval = range(1979, 2020)
file_type = '.tar.gz'
