
import sqlite3
from Initial_data_load_db import DataBaseWork
from config import db_name



data_base_work=DataBaseWork()

class StationInfo():
    """

  A class for handling station information, the information is retrieved from a database.

    """

    def station_list_by_city_user_db(self,city_name):

        """

        This code def retrieves a list of station names and addresses
        from an SQLite database based on a specified city name.

        """
        sql = "SELECT city_name,address_street,stations_id from stations where city_name = ?"
        data_base_work = DataBaseWork()
        search_result=data_base_work.db_operations(sql,(city_name,))
        return search_result

    def station_list_by_city_all_db(self):

        """This code  retrieves list of all city from db."""
        sql = 'SELECT DISTINCT(city_name) FROM stations'
        search_result=data_base_work.db_operations(sql)
        return search_result


    def sensors_list_by_station_all_db(self,stations_id):

        """This code def retrieves  all sensors by chose stations_id from db"""
        sql = "Select * from sensors where stations_id = ?"
        data_base_work = DataBaseWork()
        search_result=data_base_work.db_operations(sql,(stations_id,))
        if not search_result:
             print("Sensors list empty error.")
        return search_result

    def sensors_data_by_sensors_db(self,sensor_id):


        """This code def retrieves  all sensors_data  by chose  sensor_id from db"""

        sql = "Select * from sensors_data where sensor_id = ?"
        data_base_work = DataBaseWork()
        search_result=data_base_work.db_operations(sql,(sensor_id,))
        if not search_result:
             print("No data for this sensor")
        return search_result


    def sensors_data_by_stations_db(self,stations_id):
        sql = """select * from sensors_data as sd
    inner join sensors as s on sd.sensor_id = s.sensor_id
    inner join stations as st on st.stations_id = s.stations_id
    where st.stations_id =?"""
        data_base_work = DataBaseWork()
        search_result=data_base_work.db_operations(sql,(stations_id,))
        if not search_result:
            print("No data for this sensor")
        return search_result