import pathlib
import unittest

from services.era5_processor_service import merge_nc_files, MergeError, concatenate_nc_files

extracted_daily_data_path = 'tests/resources/extracted_daily_data'
extracted_monthly_data_path = 'tests/resources/extracted_monthly_data'


class ERA5ProcessorService(unittest.TestCase):
    def test_merge_daily_data(self):
        extracted_daily_data = pathlib.Path(extracted_daily_data_path)
        daily_files = [str(x) for x in extracted_daily_data.glob('**/*.nc') if x.is_file()]
        merge_nc_files(daily_files, 'test_daily_data.nc')
        self.assertRaises(MergeError)

    def test_concatenate_monthly_data(self):
        extracted_monthly_data = pathlib.Path(extracted_monthly_data_path)
        monthly_files = [str(x) for x in extracted_monthly_data.glob('**/*.nc') if x.is_file()]
        concatenate_nc_files(monthly_files, 'test_monthly_data.nc')
        self.assertRaises(MergeError)


if __name__ == '__main__':
    unittest.main()
