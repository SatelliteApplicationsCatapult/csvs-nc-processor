import logging

from src.services.era5_terria_catalog_generator_service import generate_terria_catalog
from src.load_config import LOG_FORMAT, LOG_LEVEL

logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)
logger = logging.getLogger(__name__)


def generate_era5_land_daily_catalog():
    logger.info("Generating Daily Catalog...")
    era5_land_daily = {
        'ERA5-Land_daily_mean_2mTemp': [1981, 2019],
        'ERA5-Land_daily_mean_RH': [1981, 2019],
        'ERA5-Land_daily_mean_TotalWind': [2001, 2019],
        'ERA5-Land_daily_total_precipitation': [1981, 2019]
    }
    for k, v in era5_land_daily.items():
        for y in range(v[0], v[1] + 1):
            generate_terria_catalog(f"{k}_{y}.nc")


def generate_era5_land_monthly_catalog():
    logger.info("Generating Monthly Catalog...")
    era5_land_monthly = {
        'ERA5-Land_monthly_mean_2mTemp': [1981, 2019],
        'ERA5-Land_monthly_mean_RH': [1981, 2019],
        'ERA5-Land_monthly_mean_TotalWind': [2001, 2019],
        'ERA5-Land_monthly_total_precipitation': [1981, 2019]
    }
    for k, v in era5_land_monthly.items():
        generate_terria_catalog(f"{k}_{v[0]}_{v[1]}.nc")


def generate_era5_land_30year_catalog():
    logger.info("Generating 30year Catalog...")
    generate_terria_catalog("ERA5-Land_30year_TotalPrecip.nc")


if __name__ == '__main__':
    generate_era5_land_daily_catalog()
    generate_era5_land_monthly_catalog()
    generate_era5_land_30year_catalog()
