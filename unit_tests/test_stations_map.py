import unittest
import os
from stations_map import StationsMap

class TestStationsMap(unittest.TestCase):

    def setUp(self):
        self.stations_map = StationsMap()

    def test_show_station_on_map_len(self):
        result = self.stations_map.show_station_on_map()
        for item in result:
            self.assertEqual(len(item), 3)

    def test_show_station_on_map_html(self):
        result = self.stations_map.show_station_on_map()
        self.assertTrue(os.path.exists('map.html'))

    def test_show_station_on_map_by_distance_long(self):
        self.test_result = self.stations_map.show_station_on_map_by_distance("New York",100)
        self.assertIsInstance(self.test_result,list)
        self.assertEqual(len(self.test_result),0)




if __name__ == '__main__':
    unittest.main()
