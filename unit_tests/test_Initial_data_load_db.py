
import unittest
import sqlite3

from config import db_name
from Initial_data_load_db import DataBaseWork


data_base_work = DataBaseWork()


class unit_test_initial_db(unittest.TestCase):
    def test_db_operations(self):
        sql = "Select * from stations"
        self.test_result = data_base_work.db_operations(sql)
        self.assertIsInstance(self.test_result, list)
        if self.test_result:
            self.assertIsInstance(self.test_result[0], tuple)
        self.assertGreater(len(self.test_result), 1)



if __name__ == '__main__':
    unittest.main()

