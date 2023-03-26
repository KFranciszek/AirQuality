#Module for retrieving station and sensor data from SQLite database.
#BUG: do porpawy pozwmykanie baz za poomocą atrybutu c.close()?
import sqlite3

class StationInfo():
#This code def retrieves a list of station names and addresses from an SQLite database based on a specified city name.
    def station_list_by_city_user_db(self,city_name):
        try:
            conn = sqlite3.connect('airquality_db.db')
            c = conn.cursor()
            c.execute(f'''SELECT city_name,address_street from stations where city_name = "{city_name}"''')
            search_result = c.fetchall()
            conn.commit()
            conn.close()
            if not search_result:
                raise ValueError("No station found for the given city name.")
            return search_result
        except sqlite3.Error as e:
            print("An error occurred while connecting to the database:", e)
            return None
        except ValueError as e:
            print("Invalid input: ", e)
            return None

#This code def retrieves  list of all city from db.
    def station_list_by_city_all_db(self):
        try:
            conn = sqlite3.connect('airquality_db.db')
            c = conn.cursor()
            c.execute(f'''Select Distinct(city_name) from stations''')
            search_result = c.fetchall()
            conn.commit()
            conn.close()
            if not search_result:
                raise ValueError("City list empty error.")
            return search_result

        except sqlite3.Error as e:
            print("An error occurred while connecting to the database:", e)
            return None

        except ValueError as e:
            print("Invalid input: ", e)
            return None

#This code def retrieves  all sensors by chose  stations_id from db.
    def sensors_list_by_station_all_db(self,stations_id):
        try:
            conn = sqlite3.connect('airquality_db.db')
            c = conn.cursor()
            c.execute(f'''Select * from sensors where stations_id = "{stations_id}"''')
            search_result = c.fetchall()
            conn.commit()
            conn.close()
            if not search_result:
                raise ValueError("Sensors list empty error.")
            return search_result

        except sqlite3.Error as e:
            print("An error occurred while connecting to the database:", e)
            return None

        except ValueError as e:
            print("Invalid input: ", e)
            return None



#This code def retrieves  all sensors_data  by chose  sensor_id from db
    def sensors_data_by_sensors_db(self,sensor_id):
        try:
            conn = sqlite3.connect('airquality_db.db')
            c = conn.cursor()
            c.execute(f'''Select * from sensors_data where sensor_id = "{sensor_id}"''')
            search_result = c.fetchall()
            conn.commit()
            conn.close()
            if not search_result:
                raise ValueError("Sensors list empty error.")
            return search_result

        except sqlite3.Error as e:
            print("An error occurred while connecting to the database:", e)
            return None

        except ValueError as e:
            print("Invalid input: ", e)
            return None



#Function that hits the database in join up to 3 tables and retrieves sensor data based on station id
    def sensors_data_by_stations_db(self,stations_id):
        try:
            conn = sqlite3.connect('airquality_db.db')
            c = conn.cursor()
            c.execute(f'''select * from sensors_data as sd
    inner join sensors as s on sd.sensor_id = s.sensor_id
    inner join stations as st on st.stations_id = s.stations_id
    where st.stations_id = "{stations_id}"''')
            search_result = c.fetchall()
            conn.commit()
            conn.close()
            if not search_result:
                raise ValueError("Sensors list empty error.")
            return search_result

        except sqlite3.Error as e:
            print("An error occurred while connecting to the database:", e)
            return None

        except ValueError as e:
            print("Invalid input: ", e)
            return None


