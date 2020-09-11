import logging
import iris
from iris.experimental.equalise_cubes import equalise_attributes
import shutil
from config import LOG_FORMAT, LOG_LEVEL, tmp_dir, std_name

logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)
logger = logging.getLogger(__name__)


def merge_nc_files(files: list, output_file: str) -> str:
    try:
        cubes = iris.load(files, callback=add_std_name_cb)
        equalise_attributes(cubes)
        logger.info('Merging files...')
        new_cube = cubes.merge_cube()
        logger.info(new_cube)
        iris.save(cubes.merge_cube(), output_file)
        return output_file
    except Exception as e:
        logger.error(f'Something happened while merging nc files: {e}')
        return ''
    finally:
        shutil.rmtree(tmp_dir)


def add_std_name_cb(cube, field, filename):
    cube.standard_name = std_name
