import pathlib
import unittest

from services.persist_state_service import update_failed_downloads, update_failed_processes, update_failed_uploads, \
    save_state


class TestPersistStateService(unittest.TestCase):

    def setUp(self) -> None:
        self.tmp_test_files = []

    def tearDown(self) -> None:
        for file in self.tmp_test_files:
            pathlib.Path(file).unlink()

    def test_update_failed_download(self):
        file_url = 'url/to/file'
        failed_downloads = update_failed_downloads(download_url=file_url)
        assert file_url in failed_downloads

    def test_update_failed_process(self):
        filename = 'tests/resources/ERA5_daily_mean_2mTemp_1979.tar.gz'
        failed_processes = update_failed_processes(tar_file_path=filename)
        assert filename in failed_processes

    def test_update_failed_upload(self):
        filename = 'tests/resources/ERA5_daily_mean_2mTemp_1979.nc'
        failed_uploads = update_failed_uploads(nc_file_path=filename)
        assert filename in failed_uploads

    def test_update_non_existing_process(self):
        filename = 'tests/resources/non_existing.tar.gz'
        failed_processes = update_failed_processes(tar_file_path=filename)
        assert filename not in failed_processes

    def test_update_non_existing_upload(self):
        filename = 'file_name_path'
        failed_uploads = update_failed_uploads(nc_file_path=filename)
        assert filename not in failed_uploads

    def test_save_state(self):
        created_file = save_state()
        self.tmp_test_files.append(created_file)
        assert pathlib.Path(created_file).exists()
