import json
import pathlib
import unittest

from services.persist_state_service import update_failed_downloads, update_failed_processes, update_failed_uploads, \
    save_state, load_state, get_state, InvalidStateFile

state_example = {
    'failed_downloads': [],
    'failed_processes': [],
    'failed_uploads': []
}

dataset_url = 'url/to/dataset.tar.gz'
valid_tar_file = 'tests/resources/ERA5_daily_mean_2mTemp_1979.tar.gz'
invalid_tar_file = 'tests/resources/non_existing.tar.gz'
valid_nc_file = 'tests/resources/ERA5_daily_mean_2mTemp_1979.nc'
invalid_nc_file = 'tests/resources/non_existing.nc'


class TestPersistStateService(unittest.TestCase):

    def setUp(self) -> None:
        self.tmp_test_files = []

    def tearDown(self) -> None:
        for file in self.tmp_test_files:
            pathlib.Path(file).unlink()

    def test_update_failed_download(self):
        failed_downloads = update_failed_downloads(download_url=dataset_url)
        assert dataset_url in failed_downloads

    def test_update_failed_process(self):
        failed_processes = update_failed_processes(tar_file_path=valid_tar_file)
        assert valid_tar_file in failed_processes

    def test_update_failed_upload(self):
        failed_uploads = update_failed_uploads(nc_file_path=valid_nc_file)
        assert valid_nc_file in failed_uploads

    def test_update_non_existing_process(self):
        failed_processes = update_failed_processes(tar_file_path=invalid_tar_file)
        assert invalid_tar_file not in failed_processes

    def test_update_non_existing_upload(self):
        failed_uploads = update_failed_uploads(nc_file_path=invalid_nc_file)
        assert invalid_nc_file not in failed_uploads

    def test_save_state(self):
        created_file = save_state(state_example)
        self.tmp_test_files.append(created_file)
        assert pathlib.Path(created_file).exists()

    def test_save_failed_uploads_state(self):
        update_failed_uploads(nc_file_path=valid_nc_file)
        state = get_state()
        created_file = save_state(state)
        self.tmp_test_files.append(created_file)
        with open(created_file, "r") as read_file:
            state = json.load(read_file)
        assert valid_nc_file in state.get('failed_uploads')

    def test_load_state(self):
        created_file = save_state(state_example)
        self.tmp_test_files.append(created_file)
        state = load_state(created_file)
        assert state.keys() == state_example.keys()

    def test_load_state_invalid_file(self):
        wrong_state_structure = {
            'something': [],
            'wrong': []
        }
        created_file = save_state(wrong_state_structure)
        self.tmp_test_files.append(created_file)
        with self.assertRaises(InvalidStateFile):
            load_state(created_file)
