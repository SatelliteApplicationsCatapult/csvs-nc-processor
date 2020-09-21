import json
import pathlib
from typing import List, Dict
from datetime import datetime

from config import log_dir

failed_downloads = []
failed_processes = []
failed_uploads = []


def update_failed_downloads(download_url: str) -> List[str]:
    failed_downloads.append(download_url)
    return failed_downloads


def update_failed_processes(tar_file_path: str) -> List[str]:
    tar_file = pathlib.Path(tar_file_path)
    if tar_file.exists():
        failed_processes.append(tar_file_path)
    return failed_processes


def update_failed_uploads(nc_file_path: str) -> List[str]:
    nc_file = pathlib.Path(nc_file_path)
    if nc_file.exists():
        failed_uploads.append(nc_file_path)
    return failed_uploads


def save_state(state: Dict[str, List]) -> str:
    state_file_name = f'state_{datetime.now().strftime("%Y-%m-%d_%H꞉%M꞉%S.%f")}.json'
    return create_state_file(state, state_file_name)


def create_state_file(state: Dict[str, List], filename: str) -> str:
    log_dir.mkdir(parents=True, exist_ok=True)
    state_file = log_dir / filename
    with open(state_file, 'w') as f_out:
        json.dump(state, f_out)
    return str(state_file)


def load_state(state_file_path: str) -> Dict[str, List]:
    with open(state_file_path, "r") as read_file:
        state = json.load(read_file)
    if not valid_state(state):
        raise InvalidStateFile(f'{state_file_path} is not a valid state file.')
    return state


def get_state():
    return {
        'failed_downloads': failed_downloads,
        'failed_processes': failed_processes,
        'failed_uploads': failed_uploads
    }


def valid_state(state: Dict[str, List]) -> bool:
    valid_state_keys = ['failed_downloads', 'failed_processes', 'failed_uploads']
    if list(state.keys()) == valid_state_keys:
        return True
    else:
        return False


class InvalidStateFile(Exception):
    """Base class for exceptions in this module."""
    pass
