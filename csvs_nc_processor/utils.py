import pathlib


def path_to_str(path: pathlib.Path) -> str:
    path_str = []
    for p in path.parts:
        path_str.append(p)
        if p != '/':
            path_str.append('/')
    return ''.join(path_str[:-1])

