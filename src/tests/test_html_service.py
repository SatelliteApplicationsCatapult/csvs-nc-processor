import unittest
from src.load_config import url
from src.services.html_service import get_html_data_list
from src.utils import make_url


class HTMLService(unittest.TestCase):
    def test_obtain_era5_daily(self):
        era5_url = make_url(url, make_url('ERA5', 'daily'))
        data_list = get_html_data_list(era5_url)
        self.assertTrue(data_list)

    def test_obtain_era5_monthly(self):
        era5_url = make_url(url, make_url('ERA5', 'monthly'))
        data_list = get_html_data_list(era5_url)
        self.assertTrue(data_list)

    def test_obtain_era5_30year(self):
        era5_url = make_url(url, make_url('ERA5', '30year'))
        data_list = get_html_data_list(era5_url)
        self.assertTrue(data_list)

    def test_obtain_era5_land_daily(self):
        era5_land_url = make_url(url, make_url('ERA5-Land', 'daily'))
        data_list = get_html_data_list(era5_land_url)
        self.assertTrue(data_list)

    def test_obtain_era5_land_monthly(self):
        era5_land_url = make_url(url, make_url('ERA5-Land', 'monthly'))
        data_list = get_html_data_list(era5_land_url)
        self.assertTrue(data_list)

    def test_obtain_era5_land_30year(self):
        era5_land_url = make_url(url, make_url('ERA5-Land', '30year'))
        data_list = get_html_data_list(era5_land_url)
        self.assertTrue(data_list)


if __name__ == '__main__':
    unittest.main()
