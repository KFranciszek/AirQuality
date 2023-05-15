
import unittest
import sqlite3

from config import db_name
from Initial_data_load_db import DataBaseWork
from station_info import StationInfo

data_base_work = DataBaseWork()
station_info = StationInfo()

class unit_test_station_info(unittest.TestCase):

    def test_station_list_by_city_all_db(self):
        self.test_result = station_info.station_list_by_city_all_db()
        self.assertIsInstance(self.test_result,list)
        if self.test_result:
            self.assertIsInstance(self.test_result[0], tuple)
        self.assertGreater(len(self.test_result), 1)

    def test_station_list_by_city_user_db(self):
        self.test_result=station_info.station_list_by_city_user_db("Warszawa")
        self.assertIsInstance(self.test_result,list)
        if self.test_result:
            self.assertIsInstance(self.test_result[0], tuple)
        self.assertGreater(len(self.test_result),1)

        self.test_result = station_info.station_list_by_city_user_db("Empty")
        self.assertIsInstance(self.test_result, list)
        self.assertEqual(len(self.test_result), 0)

if __name__ == '__main__':
    unittest.main()

