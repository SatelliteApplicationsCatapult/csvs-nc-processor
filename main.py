import iris
from iris.experimental.equalise_cubes import equalise_attributes
import os
import tarfile
import gzip
import shutil
import sys
import pathlib

tmp_dir = pathlib.Path('./.tmp')


def decompress_nc_files(tar_filepath: pathlib.Path):
    decompress_tar_file(tar_filepath, tmp_dir)
    decompressed_files = []
    files = [x for x in tmp_dir.glob('**/*') if x.is_file()]
    for file in files:
        print(f"Extracting {file.name}...")
        decompressed_files.append(decompress_gzip_file(file))
    return decompressed_files


def decompress_tar_file(filename: pathlib.Path, output_path: pathlib.Path):
    tar = tarfile.open(filename, "r:gz")
    print(f"Extracting {filename}...")
    tar.extractall(path=output_path)
    tar.close()


def decompress_gzip_file(gzip_file: pathlib.Path):
    with gzip.open(gzip_file, 'rb') as f_in:
        with open(gzip_file.with_suffix(''), 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    return gzip_file.parts[0] + '/' + gzip_file.parts[1] + '/' + gzip_file.with_suffix('').name


def merge_files(files: list, name: str, standard_name: str):
    cubes = iris.load(files, callback=add_std_name_cb)
    equalise_attributes(cubes)
    new_cube = cubes.merge_cube()
    print(new_cube)
    iris.save(cubes.merge_cube(), name)


def add_std_name_cb(cube, field, filename):
    cube.standard_name = 'air_temperature'


if __name__ == "__main__":
    try:
        filepath = pathlib.Path(sys.argv[1])
        std_name = sys.argv[2]
        output_name = filepath.name.split('.')[0] + '.nc'
        nc_files = decompress_nc_files(filepath)
        merge_files(nc_files, output_name, std_name)
    except IndexError:
        print('Usage: python main.py <filepath> <std_name>')
    finally:
        shutil.rmtree(tmp_dir)
