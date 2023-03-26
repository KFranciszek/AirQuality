#Module that converts station and air quality measurement data
import sqlite3

class DataaAnalysis():
#Function that returns the average for a specified sensor from a database
    def average_data_db(self, sensor_id):
        try:
            conn = sqlite3.connect('airquality_db.db')
            c = conn.cursor()
            c.execute(f'''Select AVG(value) from sensors_data where sensor_id = "{sensor_id}"''')
            search_result = c.fetchone()[0]
            conn.commit()
            conn.close()
            return round(search_result, 3)
        except sqlite3.Error as e:
            print("An error occurred while connecting to the database:", e)
            return None
        except ValueError as e:
            print("Invalid input: ", e)
            return None



    def smallest_largest_data_db(self, sensor_id):
#Function that returns  max and min value for a specified sensor from a database
        try:
            conn = sqlite3.connect('airquality_db.db')
            c = conn.cursor()
            c.execute(f'''Select max(value), min(value) from sensors_data where sensor_id = "{sensor_id}"''')
            search_result = c.fetchone()[:]
            conn.commit()
            conn.close()
            return ("Max value:", search_result[0], "Min value:", search_result[1])
        except sqlite3.Error as e:
            print("An error occurred while connecting to the database:", e)
            return None
        except ValueError as e:
            print("Invalid input: ", e)
            return None


