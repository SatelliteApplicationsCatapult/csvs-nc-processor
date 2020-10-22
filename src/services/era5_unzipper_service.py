import pathlib
from src.load_config import LOG_FORMAT, LOG_LEVEL, tmp_dir
import logging
import tarfile
import gzip
import shutil

logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)
logger = logging.getLogger(__name__)


def decompress_nc_files_from(tar_filepath: str) -> list:
    try:
        decompress_tar_file(pathlib.Path(tar_filepath), tmp_dir)
        decompressed_files = []
        files = [x for x in tmp_dir.glob('**/*.nc.gz') if x.is_file()]
        if files:
            for file in files:
                logger.debug(f"Extracting {file.name}...")
                decompressed_files.append(decompress_gzip_file(file))
        else:
            decompressed_files = [str(x) for x in tmp_dir.glob('**/*.nc') if x.is_file()]
        return decompressed_files
    except Exception as e:
        raise DecompressError(e)


def decompress_tar_file(filename: str, output_path: str) -> None:
    tar = tarfile.open(filename, "r:gz")
    logger.info(f"Extracting {filename}...")
    tar.extractall(path=output_path)
    tar.close()


def decompress_gzip_file(gzip_file: pathlib.Path) -> str:
    with gzip.open(gzip_file, 'rb') as f_in:
        with open(gzip_file.with_suffix(''), 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    return str(gzip_file.with_suffix(''))


class DecompressError(Exception):
    """Base class for exceptions in this module."""
    pass
