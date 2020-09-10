import pathlib


def path_to_str(path: pathlib.Path):
    path_str = []
    for p in path.parts:
        path_str.append(p)
        path_str.append('/')
    return ''.join(path_str[:-1])
