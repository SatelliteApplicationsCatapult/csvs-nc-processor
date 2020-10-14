import pathlib
from datetime import datetime, timezone, timedelta

import iris
from bokeh.core.property.datetime import Datetime
from iris.cube import CubeList, Cube


def load_cubes_from_folder(folder_path: str) -> CubeList:
    folder = pathlib.Path(folder_path)
    nc_files = [str(x) for x in folder.glob('**/*.nc') if x.is_file()]
    return iris.load(nc_files)


def get_cube_timestamp(cube: Cube) -> Datetime:
    atom_epoch = datetime(1900, 1, 1, 0, 0, tzinfo=timezone.utc)
    min_ts = atom_epoch + timedelta(hours=int(cube.aux_coords[0].bounds.min()))
    return min_ts


def make_url(*args: [str]) -> str:
    return "/".join(arg.strip("/") for arg in args)


def create_output_file(input_file: str) -> str:
    return str(pathlib.Path(input_file).with_suffix('').with_suffix('.nc'))


if __name__ == '__main__':
    cubes = load_cubes_from_folder('./daily_prec_2019')
    dates = []
    for cube in cubes:
        date = get_cube_timestamp(cube)
        if date in dates:
            print(f"{date} is already in the list")
        else:
            dates.append(date)
