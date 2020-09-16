import os
from collections import namedtuple
from logging import INFO
import pathlib

LOG_FORMAT = '%(asctime)s - %(name)12s - %(levelname)6s - %(message)s'
LOG_LEVEL = INFO

s3_url = os.getenv('S3_URL', 'url')
s3_bucket = os.getenv('S3_BUCKET', 'bucket')
s3_id = os.getenv('S3_ID', 'id')
s3_key = os.getenv('S3_KEY', 'key')

tmp_dir = pathlib.Path.cwd() / '.tmp'
std_name = {
    '2 metre temperature': 'surface_temperature',
    'Total precipitation': 'precipitation_flux',
    'Sea surface temperature': 'sea_surface_temperature',
    'Soil temperature level 1': 'soil_temperature',
    'Volumetric soil water layer 1': 'volume_fraction_of_condensed_water_in_soil'
}

climate_data_url = os.getenv('CLIMATE_DATA_URL', 'http://37.128.186.209/LAURA/ERA5/')
climate_data_to_download = {
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
DateRange = namedtuple('DareRange', ['min', 'max'])
date_range = DateRange(min=1979, max=2020)
file_type = '.tar.gz'
