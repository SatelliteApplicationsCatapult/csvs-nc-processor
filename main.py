"""Main module."""
import iris
from iris.experimental.equalise_cubes import equalise_attributes
import tarfile
import gzip
import shutil
import pathlib
import logging

from config import LOG_FORMAT, LOG_LEVEL, s3_url, s3_bucket, s3_id, s3_key,\
    tmp_dir, input_tar_file, output_nc_file, std_name

logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)
logger = logging.getLogger(__name__)


def decompress_nc_files_from(tar_filepath: pathlib.Path):
    decompress_tar_file(tar_filepath, tmp_dir)
    decompressed_files = []
    files = [x for x in tmp_dir.glob('**/*') if x.is_file()]
    for file in files:
        logger.info(f"Extracting {file.name}...")
        decompressed_files.append(decompress_gzip_file(file))
    return decompressed_files


def decompress_tar_file(filename: pathlib.Path, output_path: pathlib.Path):
    tar = tarfile.open(filename, "r:gz")
    logger.info(f"Extracting {filename}...")
    tar.extractall(path=output_path)
    tar.close()


def decompress_gzip_file(gzip_file: pathlib.Path):
    with gzip.open(gzip_file, 'rb') as f_in:
        with open(gzip_file.with_suffix(''), 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    return gzip_file.parts[0] + '/' + gzip_file.parts[1] + '/' + gzip_file.with_suffix('').name


def merge_nc_files(files: list, name: str):
    cubes = iris.load(files, callback=add_std_name_cb)
    equalise_attributes(cubes)
    new_cube = cubes.merge_cube()
    logger.info(new_cube)
    iris.save(cubes.merge_cube(), name)


def add_std_name_cb(cube, field, filename):
    cube.standard_name = std_name


def upload_to_s3(file: pathlib.Path):
    logger.info(f"Uploading {file} to {s3_url} with {s3_bucket} {s3_id} {s3_key}")


if __name__ == "__main__":
    try:
        nc_files = decompress_nc_files_from(input_tar_file)
        merge_nc_files(nc_files, output_nc_file)
        upload_to_s3(output_nc_file)
    finally:
        shutil.rmtree(tmp_dir)
