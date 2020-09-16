import logging
import iris
from iris.experimental.equalise_cubes import equalise_attributes

from src.config import LOG_FORMAT, LOG_LEVEL, std_name
import pathlib

logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)
logger = logging.getLogger(__name__)


def merge_nc_files(files: [str], output_filepath: str) -> None:
    try:
        output_file = pathlib.Path(output_filepath)
        logger.info('Merging files...')
        cubes = iris.load(files, callback=add_std_name_cb)
        equalise_attributes(cubes)
        new_cube = cubes.merge_cube()
        logger.info(new_cube)
        logger.info(f'Saving {output_file}...')
        iris.save(new_cube, str(output_file))
    except Exception as e:
        raise MergeError(e)


def add_std_name_cb(cube, field, filename):
    if cube.long_name == '2 metre temperature':
        cube.standard_name = 'surface_temperature'
    elif cube.long_name == 'Total precipitation':
        cube.standard_name = 'precipitation_flux'
    elif cube.long_name == 'Sea surface temperature':
        cube.standard_name = 'sea_surface_temperature'
    elif cube.long_name == 'Soil temperature level 1':
        cube.standard_name = 'soil_temperature'
    elif cube.long_name == 'Volumetric soil water layer 1':
        cube.standard_name = 'volume_fraction_of_condensed_water_in_soil'


class MergeError(Exception):
    """Base class for exceptions in this module."""
    pass
