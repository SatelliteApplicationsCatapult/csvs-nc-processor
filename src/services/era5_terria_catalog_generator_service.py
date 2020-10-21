from typing import Dict

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


def generate_terria_catalog(filepath: str) -> Dict:
    catalog_entry = generate_terria_catalog_era5_entry(filepath)
    new_terria_catalog = add_entry_to_terria_catalog(catalog_entry)
    save_terria_catalog_file(new_terria_catalog)
    return new_terria_catalog


def generate_terria_catalog_era5_entry(filepath: str) -> Dict:
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
            f'latitude={{{{terria.coords.latitude}}}}&'
            f'longitude={{{{terria.coords.longitude}}}}&'
            f'time_start={time_start}&'
            f'time_end={time_end}&'
            f'accept=csv\" y-column=\"3\" hide-buttons=\"True\"></chart>',
        'colorScaleMinimum': color_min,
        'colorScaleMaximum': color_max,
        'layers': var,
        'url': f"{thredds_url}/wms/{dataset}/{file.name}?service=WMS&version=1.3.0&request=GetCapabilities"
    }


def get_variable_name(filename: str) -> str:
    return [v for k, v in variable_names.items() if k in filename][0]


def calculate_color_scale_range(filepath: str) -> [int, int]:
    cube = iris.load_cube(filepath)
    mean_over_time = cube.collapsed('time', iris.analysis.MEAN)
    return int(mean_over_time.data.min()), int(mean_over_time.data.max())


def get_default_color_scale_rage(filename: str) -> [int, int]:
    return [v for k, v in color_scale_ranges.items() if k in filename][0]


def add_entry_to_terria_catalog(entry: Dict) -> Dict:
    """ Adds the terria catalog entry to catalog and returns the new catalog"""
    terria_catalog = load_terria_catalog_yaml()

    group_entry = [d.get('items') for d in terria_catalog.get('catalog') if d.get('name') in entry.get('name')]
    if not group_entry:
        pass
        # TODO: Create group for this data
    subgroup_entry = [d.get('items') for d in group_entry[0] if d.get('name') in entry.get('name')]
    if not subgroup_entry:
        pass
        # TODO: Create subgroup for this data
    terria_catalog.get('catalog').append(group_entry.append(subgroup_entry[0].append(entry)))

    return terria_catalog


def load_terria_catalog_yaml() -> Dict:
    """ Load terria catalog yml file and return it as a dictionary """
    with open(terria_catalog_yaml) as file:
        terria_catalog = yaml.load(file, Loader=yaml.FullLoader)
    return terria_catalog


def save_terria_catalog_file(terria_catalog: Dict):
    with open(new_terria_catalog_yaml, 'w') as file:
        catalog = yaml.dump(terria_catalog, file)
    print(catalog)
    return catalog


if __name__ == '__main__':
    generate_terria_catalog('ERA5-Land_daily_mean_2mTemp_2019.nc')
