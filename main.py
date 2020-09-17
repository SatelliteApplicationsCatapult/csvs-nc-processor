"""Main module."""
import logging
from config import LOG_FORMAT, LOG_LEVEL, climate_data_to_download, date_range, tmp_dir
from services.era5_unzipper_service import decompress_nc_files_from, DecompressError
from services.era5_processor_service import merge_nc_files, MergeError
from services.s3_uploader_service import upload_to_s3, UploadError
from services.era5_downloader_service import create_output_file, get_input_occurrences, get_era5_url_suffixes, \
    download_era5_files
import shutil

logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)
logger = logging.getLogger(__name__)


def main():
    try:
        occurrences = get_input_occurrences(era5_url_structure=climate_data_to_download)
        for occurrence in occurrences:
            data_products = climate_data_to_download[occurrence]
            era5_url_suffixes = get_era5_url_suffixes(data_products=data_products, date_range=date_range)
            for filename in download_era5_files(occurrence=occurrence, url_suffixes=era5_url_suffixes):
                try:
                    output_nc_file = process_era5_data(filename)
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


def process_era5_data(filename: str) -> str:
    nc_files = decompress_nc_files_from(filename)
    output_nc_file = create_output_file(filename)
    merge_nc_files(nc_files, output_nc_file)
    return output_nc_file


if __name__ == "__main__":
    main()
