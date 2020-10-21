from typing import Dict, Tuple

import iris.analysis
import iris
import yaml
import pathlib

variable_names = {
    '2mTemp': 't2m',
    'RH': 't2m',
    'TotalWind': 'u10',
    'mslp': 'msl',
    'soil_temp': 'stl1',
    'soil_water': 'swvl1',
    'sol_rad': 'ssr',
    'total_precipitation': 'precipitation_rate',
    'monthly_precipitation': 'tp'
}

color_scale_ranges = {
    '2mTemp': [-50, 50],
    'RH': [0, 100],
    'TotalWind': [0, 13],
    'mslp': [96500, 104000],
    'soil_temp': [-50, 50],
    'soil_water': [0, 1],
    'sol_rad': [25860, 1291000],
    'total_precipitation': [0, 1000]
}

terria_catalog_yaml = './tests/resources/terria_catalog.yaml'
new_terria_catalog_yaml = './tests/resources/new_terria_catalog.yaml'


def generate_terria_catalog(filepath: str) -> dict:
    catalog_entry = generate_terria_catalog_era5_entry(filepath)
    new_terria_catalog = add_entry_to_terria_catalog(catalog_entry)
    save_terria_catalog_file(new_terria_catalog)
    return new_terria_catalog


def generate_terria_catalog_era5_entry(filepath: str) -> dict:
    file = pathlib.Path(filepath)
    filename = file.stem
    dataset = "_".join(filename.split('_')[:4])
    year = filename.split('_')[4]
    name = filename.replace('_', ' ')
    var = get_variable_name(filename)
    # color_min, color_max = calculate_color_scale_range(filepath)
    color_min, color_max = get_default_color_scale_rage(filename)
    time_start = f"{year}-01-01T11:00:00Z"
    time_end = f"{year}-12-31T11:00:00Z"
    thredds_url = "http://thredds:8080/thredds"

    return {
        'name': name,
        'type': 'wms',
        'featureInfoTemplate':
            f'<p>{name}</p><chart src=\"{thredds_url}/ncss/{dataset}/{file.name}?'
            f'var={var}&'
            'latitude={{terria.coords.latitude}}&'
            'longitude={{terria.coords.longitude}}&'
            f'time_start={time_start}&'
            f'time_end={time_end}&'
            'accept=csv\" y-column=\"3\" hide-buttons=\"True\"></chart>',
        'colorScaleMinimum': color_min,
        'colorScaleMaximum': color_max,
        'layers': var,
        'url': f"{thredds_url}/wms/{dataset}/{file.name}?service=WMS&version=1.3.0&request=GetCapabilities"
    }


def get_variable_name(filename: str) -> str:
    return [v for k, v in variable_names.items() if k in filename][0]


def calculate_color_scale_range(filepath: str) -> Tuple[int, int]:
    cube = iris.load_cube(filepath)
    mean_over_time = cube.collapsed('time', iris.analysis.MEAN)
    return int(mean_over_time.data.min()), int(mean_over_time.data.max())


def get_default_color_scale_rage(filename: str) -> [int, int]:
    return [v for k, v in color_scale_ranges.items() if k in filename][0]


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


def save_terria_catalog_file(terria_catalog: dict):
    with open(new_terria_catalog_yaml, 'w') as file:
        yaml.dump(terria_catalog, file)
