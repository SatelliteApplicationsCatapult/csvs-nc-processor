"""Main module."""
import iris
from iris.experimental.equalise_cubes import equalise_attributes
import tarfile
import gzip
import shutil
import pathlib
import logging
import boto3
from botocore.exceptions import ClientError

from config import LOG_FORMAT, LOG_LEVEL, s3_url, s3_bucket, s3_id, s3_key, \
    tmp_dir, input_tar_file, output_nc_file, std_name

logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)
logger = logging.getLogger(__name__)


def decompress_nc_files_from(tar_filepath: pathlib.Path):
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
        return False


def decompress_tar_file(filename: pathlib.Path, output_path: pathlib.Path):
    try:
        tar = tarfile.open(filename, "r:gz")
        logger.info(f"Extracting {filename}...")
        tar.extractall(path=output_path)
        tar.close()
    except Exception as e:
        logger.error(f'Something happened while decompressing {filename}: {e}')


def decompress_gzip_file(gzip_file: pathlib.Path):
    with gzip.open(gzip_file, 'rb') as f_in:
        with open(gzip_file.with_suffix(''), 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    return path_to_str(gzip_file.with_suffix(''))


def merge_nc_files(files: list, output_file: str):
    try:
        cubes = iris.load(files, callback=add_std_name_cb)
        equalise_attributes(cubes)
        new_cube = cubes.merge_cube()
        logger.info(new_cube)
        iris.save(cubes.merge_cube(), output_file)
        return output_file
    except Exception as e:
        logger.error(f'Something happened while merging nc files: {e}')
        return False
    finally:
        shutil.rmtree(tmp_dir)


def add_std_name_cb(cube, field, filename):
    cube.standard_name = std_name


def upload_to_s3(filepath: pathlib.Path):
    logger.info(f"Uploading {file} to {s3_bucket} bucket...")
    s3_client = boto3.client('s3', endpoint_url=s3_url, aws_access_key_id=s3_id,
                             aws_secret_access_key=s3_key)
    try:
        s3_client.upload_file(path_to_str(filepath), s3_bucket, filepath.name)
    except ClientError as e:
        logger.error(e)
    finally:
        output_nc_file.unlink()


def path_to_str(path: pathlib.Path):
    path_str = []
    for p in path.parts:
        path_str.append(p)
        path_str.append('/')
    return ''.join(path_str[:-1])


if __name__ == "__main__":
    try:
        nc_files = decompress_nc_files_from(input_tar_file)
        if nc_files:
            file = merge_nc_files(nc_files, output_nc_file)
            if file:
                upload_to_s3(output_nc_file)
    except Exception as e:
        logger.error(e)
