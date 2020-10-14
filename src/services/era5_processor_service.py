import logging
import iris
from iris.experimental.equalise_cubes import equalise_attributes

from load_config import LOG_FORMAT, LOG_LEVEL, std_name
import pathlib
from utils import create_output_file

logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)
logger = logging.getLogger(__name__)


def process_era5_data(nc_files: [str], filename: str) -> str:
    output_nc_file = create_output_file(filename)
    if 'daily' in filename:
        merge_nc_files(nc_files, output_nc_file)
    elif 'monthly' in filename:
        concatenate_nc_files(nc_files, output_nc_file)
    return output_nc_file


def merge_nc_files(files: [str], output_filepath: str) -> None:
    try:
        output_file = pathlib.Path(output_filepath)
        logger.info('Loading cubes...')
        cubes = iris.load(files, callback=add_std_name_cb)
        logger.info('Merging files...')
        equalise_attributes(cubes)
        new_cube = cubes.merge_cube()
        logger.info(new_cube)
        logger.info(f'Saving {output_file}...')
        iris.save(new_cube, str(output_file))
    except Exception as e:
        raise MergeError(e)


def concatenate_nc_files(files: [str], output_filepath: str) -> None:
    try:
        output_file = pathlib.Path(output_filepath)
        logger.info('Loading cubes...')
        cubes = iris.load(files, callback=add_std_name_cb)
        logger.info('Concatenating files...')
        new_cube = cubes.concatenate()
        logger.info(new_cube[0])
        logger.info(f'Saving {output_file}...')
        iris.save(new_cube[0], str(output_file))
    except Exception as e:
        raise MergeError(e)


def add_std_name_cb(cube, field, filename):
    if cube.standard_name is None:
        if std_name.get(cube.long_name) is not None:
            cube.standard_name = std_name[cube.long_name]


class MergeError(Exception):
    """Base class for exceptions in this module."""
    pass
