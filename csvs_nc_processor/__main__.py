"""Main module."""
import logging
from config import LOG_FORMAT, LOG_LEVEL, input_tar_file, output_nc_file
from unzipper import decompress_nc_files_from
from processor import merge_nc_files
from uploader import upload_to_s3
from downloader import obtain_files

logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)
logger = logging.getLogger(__name__)


if __name__ == "__main__":
    try:
        for input_tar_file in obtain_files():
            nc_files = decompress_nc_files_from(input_tar_file)
            if nc_files:
                file = merge_nc_files(nc_files, output_nc_file)
                if file:
                    upload_to_s3(output_nc_file)
    except Exception as e:
        logger.error(e)
