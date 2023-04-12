#The code is vulnerable to SQL injection attacks because it uses f-strings to construct SQL queries. Instead, use parameterized queries.
#The connection and cursor handling can be improved by using context managers (the with statement). This ensures that resources are released properly, even if an exception occurs.
#There is code repetition in each method for connecting to the database, executing queries, and handling errors. This can be refactored into a separate method to avoid repetition and make the code more maintainable.

#Module for retrieving station and sensor data from SQLite database.


import sqlite3
from Initial_data_load_db import DataBaseWork
from config import db_name


class StationInfo():
#This code def retrieves a list of station names and addresses from an SQLite database based on a specified city name.
    def station_list_by_city_user_db(self,city_name):
        data_base_work = DataBaseWork()
        conn, c = data_base_work.connect_db()
        sql = "SELECT city_name,address_street,stations_id from stations where city_name = ?"
        data_base_work.execute_sql(conn, c, sql,(city_name,))
        search_result = c.fetchall()
        conn.commit()
        conn.close()
        if not search_result:
            raise ValueError("No station found for the given city name.")
        return search_result

    def station_list_by_city_all_db(self):
        # This code def retrieves  list of all city from db.
        data_base_work = DataBaseWork()
        conn, c = data_base_work.connect_db()
        sql = 'SELECT DISTINCT(city_name) FROM stations'
        data_base_work.execute_sql(conn, c, sql)
        search_result = c.fetchall()
        conn.commit()
        c.close()
        conn.close()
        return search_result

    def sensors_list_by_station_all_db(self,stations_id):
# This code def retrieves  all sensors by chose  stations_id from db.
        data_base_work = DataBaseWork()
        conn, c = data_base_work.connect_db()
        sql = "Select * from sensors where stations_id = ?"
        data_base_work.execute_sql(conn, c, sql,(stations_id,))
        search_result = c.fetchall()
        conn.commit()
        conn.close()
        if not search_result:
            raise ValueError("Sensors list empty error.")
        return search_result

    def sensors_data_by_sensors_db(self,sensor_id):
 # This code def retrieves  all sensors_data  by chose  sensor_id from db
        data_base_work = DataBaseWork()
        conn, c = data_base_work.connect_db()
        sql = "Select * from sensors_data where sensor_id = ?"
        data_base_work.execute_sql(conn, c, sql,(sensor_id,))
        search_result = c.fetchall()
        conn.commit()
        conn.close()
        if not search_result:
            raise ValueError("Sensors data list empty error.")
        return search_result


    def sensors_data_by_stations_db(self,stations_id):
# Function that hits the database in join up to 3 tables and retrieves sensor data based on station id
        data_base_work = DataBaseWork()
        conn, c = data_base_work.connect_db()
        sql = """select * from sensors_data as sd
    inner join sensors as s on sd.sensor_id = s.sensor_id
    inner join stations as st on st.stations_id = s.stations_id
    where st.stations_id =?"""
        data_base_work.execute_sql(conn, c, sql, (stations_id,))
        search_result = c.fetchall()
        conn.commit()
        conn.close()
        if not search_result:
            raise ValueError("Sensors data list empty error.")
        return search_result
