import pathlib
from datetime import datetime, timezone, timedelta

import iris
from bokeh.core.property.datetime import Datetime
from iris.cube import CubeList, Cube
from src.load_config import url, datasets, occurrences, product_filter
from src.services.html_service import get_html_data_list


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


def obtain_products_url():
    products = []
    for dataset in datasets:
        for occurrence in occurrences:
            occurrence_url = make_url(url, dataset, occurrence)
            products_url = [make_url(occurrence_url, p) for p in get_html_data_list(occurrence_url)]
            products.extend(products_url)
    return [p for p in products if product_filter in p]
