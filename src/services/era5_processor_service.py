import logging
import iris
from iris.cube import CubeList
from iris.experimental.equalise_cubes import equalise_attributes

from load_config import LOG_FORMAT, LOG_LEVEL, std_name, aoi, units, long_names
from utils import create_output_file

logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)
logger = logging.getLogger(__name__)


def process_era5_data(nc_files: [str], filename: str) -> str:
    output_nc_file = create_output_file(filename)
    logger.info('Loading cubes...')
    cubes = iris.load(nc_files, callback=add_std_name_cb).extract(
        iris.Constraint(coord_values={'latitude': lambda cell: aoi['latitude'][0] < cell < aoi['latitude'][1],
                                      'longitude': lambda cell: aoi['longitude'][0] < cell < aoi['longitude'][1]})
    )
    if 'daily' in filename:
        merge_nc_files(cubes, output_nc_file)
    else:
        concatenate_nc_files(cubes, output_nc_file)


    return output_nc_file


def merge_nc_files(cubes: CubeList, output_filepath: str) -> None:
    try:
        logger.info('Merging files...')
        equalise_attributes(cubes)
        new_cube = cubes.merge_cube()
        logger.info(new_cube)
        logger.info(f'Saving {output_filepath}...')
        iris.save(new_cube, output_filepath)
    except Exception as e:
        raise MergeError(e)


def concatenate_nc_files(cubes: CubeList, output_filepath: str) -> None:
    try:
        logger.info('Concatenating files...')
        new_cube = cubes.concatenate()
        logger.info(new_cube[0])
        logger.info(f'Saving {output_filepath}...')
        iris.save(new_cube[0], output_filepath)
    except Exception as e:
        raise MergeError(e)


def add_std_name_cb(cube, field, filename):
    if cube.standard_name is None:
        if std_name.get(cube.long_name) is not None:
            cube.standard_name = std_name[cube.long_name]
    if long_names.get(cube.standard_name) is not None:
        cube.long_name = long_names[cube.standard_name]
    cube.convert_units(units[cube.standard_name])


class MergeError(Exception):
    """Base class for exceptions in this module."""
    pass
