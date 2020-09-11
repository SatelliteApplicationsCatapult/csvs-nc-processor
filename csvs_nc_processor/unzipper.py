import pathlib
from config import LOG_FORMAT, LOG_LEVEL, tmp_dir
import logging
import tarfile
import gzip
import shutil
from utils import path_to_str

logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)
logger = logging.getLogger(__name__)


def decompress_nc_files_from(tar_filepath: pathlib.Path) -> list:
    try:
        decompress_tar_file(tar_filepath, tmp_dir)
        decompressed_files = []
        files = [x for x in tmp_dir.glob('**/*') if x.is_file()]
        for file in files:
            logger.info(f"Extracting {file.name}...")
            decompressed_files.append(decompress_gzip_file(file))
        return decompressed_files
    except Exception as e:
        logger.error(f'Something happened while decompressing: {e}')
        return []


def decompress_tar_file(filename: pathlib.Path, output_path: pathlib.Path) -> None:
    try:
        tar = tarfile.open(filename, "r:gz")
        logger.info(f"Extracting {filename}...")
        tar.extractall(path=output_path)
        tar.close()
    except Exception as e:
        logger.error(f'Something happened while decompressing {filename}: {e}')


def decompress_gzip_file(gzip_file: pathlib.Path) -> str:
    with gzip.open(gzip_file, 'rb') as f_in:
        with open(gzip_file.with_suffix(''), 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    return path_to_str(gzip_file.with_suffix(''))
