"""Main module."""
import logging
from load_config import LOG_FORMAT, LOG_LEVEL, tmp_dir, url, datasets, \
    occurrences, product_list
from services.era5_unzipper_service import decompress_nc_files_from, DecompressError
from services.era5_processor_service import MergeError, process_era5_data
from services.html_service import get_html_data_list
from services.s3_uploader_service import upload_to_s3, UploadError
from services.era5_downloader_service import download_products
import shutil

from utils import make_url

logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)
logger = logging.getLogger(__name__)


def main():
    try:
        for dataset in datasets:
            for occurrence in occurrences:
                occurrence_url = make_url(url, dataset, occurrence)
                if not product_list:
                    products = get_html_data_list(occurrence_url)
                else:
                    products = product_list
                for filename in download_products(data_url=occurrence_url, products=products):
                    try:
                        nc_files = decompress_nc_files_from(filename)
                        output_nc_file = process_era5_data(nc_files, filename)
                        upload_to_s3(output_nc_file)
                    except UploadError as ue:
                        logger.error(f"Error occurred trying to upload {filename}: {ue}")
                    except DecompressError as de:
                        logger.error(f"Error decompressing {filename}: {de}")
                    except MergeError as me:
                        logger.error(f"Error merging {filename}: {me}")
                    finally:
                        shutil.rmtree(tmp_dir)
    except Exception as e:
        logger.error(e)


if __name__ == "__main__":
    main()
