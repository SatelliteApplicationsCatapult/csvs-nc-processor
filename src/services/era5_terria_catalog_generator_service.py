from typing import Tuple

import iris.analysis
import iris
import yaml
import pathlib

from src.load_config import variable_names, color_scale_ranges, terria_catalog_yaml, styles


def generate_terria_catalog(filepath: str) -> dict:
    catalog_entry = generate_terria_catalog_era5_entry(filepath)
    new_terria_catalog = add_entry_to_terria_catalog(catalog_entry)
    save_terria_catalog_file(new_terria_catalog, terria_catalog_yaml)
    return new_terria_catalog


def generate_terria_catalog_era5_entry(filepath: str) -> dict:
    file = pathlib.Path(filepath)
    filename = file.stem
    dataset_root = get_dataset_root(filename)
    product_key_name = get_product_key_name(filename)
    name = filename.replace('_', ' ')
    var = variable_names.get(product_key_name)
    # color_min, color_max = calculate_color_scale_range(filepath)
    color_min, color_max = color_scale_ranges.get(product_key_name)
    time_start, time_end = get_start_end_dates(filename)
    thredds_url = "http://thredds:8080/thredds"
    style = styles.get(product_key_name)

    return {
        'name': name,
        'type': 'wms',
        'featureInfoTemplate':
            f'<p>{name}</p><chart src=\"{thredds_url}/ncss/{dataset_root}/{file.name}?'
            f'var={var}&'
            'latitude={{terria.coords.latitude}}&'
            'longitude={{terria.coords.longitude}}&'
            f'time_start={time_start}&'
            f'time_end={time_end}&'
            'accept=csv\" y-column=\"3\" hide-buttons=\"True\"></chart>',
        'colorScaleMinimum': color_min,
        'colorScaleMaximum': color_max,
        'layers': var,
        'url': f"{thredds_url}/wms/{dataset_root}/{file.name}?service=WMS&version=1.3.0&request=GetCapabilities",
        'style': style
    }


def get_product_key_name(filename: str) -> str:
    occurrence_key = filename.split('_')[1]
    occurrences = {
        'daily': get_product_key_name_daily,
        'monthly': get_product_key_name_monthly,
        '30year': get_product_key_name_30year
    }
    return occurrences.get(occurrence_key)(filename)


def get_product_key_name_daily(filename: str) -> str:
    return '_'.join(filename.split('_')[2:4])


def get_product_key_name_monthly(filename: str) -> str:
    return '_'.join(filename.split('_')[2:-2])


def get_product_key_name_30year(filename: str) -> str:
    return '_'.join(filename.split('_')[2:])


def get_dataset_root(filename: str) -> str:
    occurrence_key = filename.split('_')[1]
    occurrences = {
        'daily': get_dataset_root_daily,
        'monthly': get_dataset_root_monthly_30year,
        '30year': get_dataset_root_monthly_30year
    }
    return occurrences.get(occurrence_key)(filename)


def get_start_end_dates(filename: str) -> Tuple[str, str]:
    occurrence_key = filename.split('_')[1]
    occurrences = {
        'daily': get_start_end_dates_daily,
        'monthly': get_start_end_dates_monthly,
        '30year': get_start_end_dates_30year
    }
    return occurrences.get(occurrence_key)(filename)


def get_start_end_dates_daily(filename: str) -> Tuple[str, str]:
    return f"{filename.split('_')[4]}-01-01T11:00:00Z", \
           f"{filename.split('_')[4]}-12-31T11:00:00Z"


def get_start_end_dates_monthly(filename: str) -> Tuple[str, str]:
    return f"{filename.split('_')[4]}-01-16T12:00:00Z", \
           f"{filename.split('_')[5]}-12-16T11:30:00Z"


def get_start_end_dates_30year(filename: str) -> Tuple[str, str]:
    return "1995-07-03T12:00:00Z", \
           "1996-07-01T11:00:00Z"


def get_dataset_root_daily(filename: str) -> str:
    return "_".join(filename.split('_')[:4])


def get_dataset_root_monthly_30year(filename: str) -> str:
    return "_".join(filename.split('_')[:2])


def calculate_color_scale_range(filepath: str) -> Tuple[int, int]:
    cube = iris.load_cube(filepath)
    mean_over_time = cube.collapsed('time', iris.analysis.MEAN)
    return int(mean_over_time.data.min()), int(mean_over_time.data.max())


def add_entry_to_terria_catalog(entry: dict) -> dict:
    """ Adds the terria catalog entry to catalog and returns the new catalog"""
    terria_catalog = load_terria_catalog_yaml()

    group_name = ' '.join(entry.get('name').split(' ')[:2])
    group_entries = get_group_entries(group_name, terria_catalog.get('catalog'))

    subgroup_name = ' '.join(entry.get('name').split(' ')[:4])
    subgroup_entries = get_group_entries(subgroup_name, group_entries)

    subgroup_entries.append(entry)

    return terria_catalog


def get_group_entries(group_name: str, groups: list) -> list:
    group = [d for d in groups if d.get('name', ' ') == group_name]
    if not group:
        groups.append({
            'name': group_name,
            'type': 'group',
            'preserveOrder': True,
            'isOpen': False,
            'items': []
        })
        group = [d for d in groups if d.get('name') == group_name]
    return group[0].get('items')


def load_terria_catalog_yaml() -> dict:
    """ Load terria catalog yml file and return it as a dictionary """
    with open(terria_catalog_yaml) as file:
        terria_catalog = yaml.load(file, Loader=yaml.FullLoader)
    return terria_catalog


def save_terria_catalog_file(terria_catalog: dict, file: str):
    with open(file, 'w') as f:
        yaml.dump(terria_catalog, f)
