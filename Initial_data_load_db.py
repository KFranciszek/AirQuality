#bug zabezpiecz każda baze na diplikaty jak inne.
import cmath
#import curses
import requests
import json
import sqlite3

#Module that creates tables for the application and runs their initial feed from the API

class DataBaseWork():
    #Function that creates 3 tables
    def db_create(self):
        try:
            conn = sqlite3.connect('airquality_db_test2.db')
            c = conn.cursor()
            c.execute('''CREATE TABLE "sensors" (
            "sensor_id"	INT,
            "stations_id"	INT,
            "param_name"	VARCHAR(255),
            "param_formula"	VARCHAR(20),
            "param_code"	VARCHAR(20),
            "param_id"	INT
            )''')
            conn.commit()
            c.execute('''CREATE TABLE "sensors_data" (
            "sensor_id"	INT,
            "key"	VARCHAR(20),
            "date"	datetime,
            "value"	INT,
             UNIQUE(sensor_id, key, date, value))''')
            conn.commit()
            c.execute('''CREATE TABLE "stations" (
            "stations_id"	INT,
            "station_name"	VARCHAR(255),
            "gegr_lat"	VARCHAR(20),
            "gegr_lon"	VARCHAR(20),
            "city_id"	INT,
            "city_name"	VARCHAR(255),
            "commune_name"	VARCHAR(255),
            "district_name"	VARCHAR(255),
            "province_name"	VARCHAR(255),
            "address_street" VARCHAR(255))''')
            conn.commit()
            c.close()
            conn.close()
        except (sqlite3.OperationalError,sqlite3.Error,) as e:
            print("db error:",e)

    def initial_payment_stations(self):
        #Initial load data from API, stations table.
        try:
            api_url = 'https://api.gios.gov.pl/pjp-api/rest/station/findAll'
            response = requests.get(api_url)
            data = response.json()
        except requests.exceptions.RequestException as e:
            print("An error occurred while making the request:", e)

        try:
            conn = sqlite3.connect('airquality_db_test2.db',timeout=1500)
            c = conn.cursor()
            for station in data:
                city = station['city']
                commune = city['commune']
                c.execute('''INSERT INTO stations
                             (stations_id, station_name, gegr_lat, gegr_lon, city_id,
                              city_name, commune_name, district_name,
                              province_name, address_street)
                             VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                          (station['id'], station['stationName'], station['gegrLat'],
                           station['gegrLon'], city['id'], city['name'],
                           commune['communeName'], commune['districtName'],
                           commune['provinceName'], station['addressStreet']))
            conn.commit()
            c.close()
            conn.close()

        except sqlite3.Error as e:
            print("An error occurred while connecting to the database:", e)





    def initial_payment_sensors(self):
        #Initial load data from API, sensors table.
        try:
            api_url = 'https://api.gios.gov.pl/pjp-api/rest/station/findAll'
            response = requests.get(api_url)
        except requests.exceptions.RequestException as e:
            print("An error occurred while making the request:", e)
        data = response.json()
        ids = [station['id'] for station in data]
        sensors_data = []
        for i in ids:
            api_url = 'https://api.gios.gov.pl/pjp-api/rest/station/sensors/'
            api_url = api_url + str(i)
            response = requests.get(api_url)
            data = response.json()
            sensors_data.append(data)
            conn = sqlite3.connect('airquality_db_test2.db')
            c = conn.cursor()
            for sensor in data:
                try:
                    c.execute('''INSERT INTO sensors
                                 (sensor_id,stations_id, param_name, param_formula, param_code,
                                  param_id)
                                 VALUES (?,?, ?, ?, ?,?)''',
                              (sensor['id'],sensor['stationId'], sensor['param']['paramName'],
                               sensor['param']['paramFormula'], sensor['param']['paramCode'], sensor['param']['idParam']
                                       ))

                    conn.commit()

                except sqlite3.Error as e:
                    print("An error occurred while connecting to the database:", e)
            c.close()
            conn.close()


#BUG:Do poprawy unikalność rekordów data
    def initial_payment_getData(self):
        # Initial load data from API, sensors data table.
        try:
            api_url = 'https://api.gios.gov.pl/pjp-api/rest/station/findAll'
            response = requests.get(api_url)
        except requests.exceptions.RequestException as e:
            print("An error occurred while making the request:", e)
        data = response.json()
        ids = [station['id'] for station in data]
        api_url = 'https://api.gios.gov.pl/pjp-api/rest/station/sensors/'
        sensors_data = [requests.get(api_url + str(i)).json() for i in ids]
        ids_sensors = [s['id'] for lst in sensors_data for s in lst]
        api_url = 'https://api.gios.gov.pl/pjp-api/rest/data/getData/'
        sensors_data = [{'sensor_id':i,'data':requests.get(api_url + str(i)).json()} for i in ids_sensors]
        conn = sqlite3.connect('airquality_db_test2.db')
        c = conn.cursor()
        inserted_rows_count = 0
        for i in sensors_data:
            try:
                sensor_id = i['sensor_id']
                data = i['data']
                key = data['key']
                for value in data['values']:

                    date = value['date']
                    value = value['value']
                    c.execute("INSERT OR IGNORE INTO sensors_data (sensor_id, key,date, value) VALUES (?, ?, ?,?)",
                              (sensor_id, key,date, value))
                    conn.commit()
                    inserted_rows_count+=1
            except sqlite3.Error as e:
                print("An error occurred while connecting to the database:", e)

        c.close()
        conn.close()
        print(f"Total rows inserted: {inserted_rows_count}")



DataBaseWork_db= DataBaseWork()
#DataBaseWork_db_c = DataBaseWork_db.db_create()
DataBaseWork_db_c = DataBaseWork_db.initial_payment_sensors()