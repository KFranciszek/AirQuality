
import requests
import json
import sqlite3
from config import db_name
from  api_conect import api_connecting

class DataBaseWork:
    """

    A collection of functions that work with the database from establishing a connection,
    executing a query on the database to a series of actions like initial load

    """

    def connect_db(self):
        """

        Establishing a connection to the database

        """
        db_name
        conn = sqlite3.connect(db_name)
        c = conn.cursor()
        return conn, c

    def execute_sql(self,conn,c,sql,values=None):

        """

        Executing a query on the database

        """
        if values:
            c.execute(sql, values)
        else:
            c.execute(sql)


    def db_operations(self):
        db_name
        with sqlite3.connect(db_name) as coon:
            conn = sqlite3.connect(db_name)
            if values:
                c.execute(sql, values)
            else:
                c.execute(sql)




    def db_create(self):

        """Creation of 3 specific databases"""

        try:
            db_name
            #connect_db()
            conn, c = self.connect_db()
            sql1 = '''CREATE TABLE "sensors" (
                "sensor_id"	INT,
                "stations_id"	INT,
                "param_name"	VARCHAR(255),
                "param_formula"	VARCHAR(20),
                "param_code"	VARCHAR(20),
                "param_id"	INT,
                 UNIQUE(sensor_id,stations_id,param_name,param_formula,param_code,param_id))'''
            sql2 = '''CREATE TABLE "sensors_data" (
                "sensor_id"	INT,
                "key"	VARCHAR(20),
                "date"	datetime,
                "value"	INT,
                 UNIQUE(sensor_id, key, date, value))'''
            sql3 = '''CREATE TABLE "stations" (
                "stations_id"	INT,
                "station_name"	VARCHAR(255),
                "gegr_lat"	VARCHAR(20),
                "gegr_lon"	VARCHAR(20),
                "city_id"	INT,
                "city_name"	VARCHAR(255),
                "commune_name"	VARCHAR(255),
                "district_name"	VARCHAR(255),
                "province_name"	VARCHAR(255),
                "address_street" VARCHAR(255),
                 UNIQUE(stations_id,station_name,gegr_lat,gegr_lon,city_id,city_name,
                 commune_name,district_name,province_name,address_street))'''
            sql = [sql1,sql2,sql3]
            for i in sql:
                self.execute_sql(conn, c, i)
                conn.commit()
        except (sqlite3.OperationalError,sqlite3.Error,) as e:
            print("db error:",e)


    def initial_payment_stations(self):

        """Call station/findAll API fetch data and flip to station table"""

        api_url = 'https://api.gios.gov.pl/pjp-api/rest/station/findAll'
        response = api_connecting(api_url)
        data = response.json()
        conn, c = self.connect_db()
        for station in data:
            city = station['city']
            commune = city['commune']
            sql = '''INSERT OR IGNORE INTO stations
                         (stations_id, station_name, gegr_lat, gegr_lon, city_id,
                          city_name, commune_name, district_name,
                          province_name, address_street)
                         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
            values = (station['id'], station['stationName'], station['gegrLat'],
                      station['gegrLon'], city['id'], city['name'],
                      commune['communeName'], commune['districtName'],
                      commune['provinceName'], station['addressStreet'])
            self.execute_sql(conn, c, sql, values)
        conn.commit()
        c.close()
        conn.close()



    def initial_payment_sensors(self):

        """Call station/findAll API to  get all stationsID,
        next  use stationID to  call station/sensors/ and fetch data to sensors tabel"""


        api_url = 'https://api.gios.gov.pl/pjp-api/rest/station/findAll'
        response = api_connecting(api_url)
        data = response.json()
        ids = [station['id'] for station in data]
        sensors_data = []
        for i in ids:
            api_url = 'https://api.gios.gov.pl/pjp-api/rest/station/sensors/'
            api_url = api_url + str(i)
            response = api_connecting(api_url)
            data = response.json()
            sensors_data.append(data)
            conn, c = self.connect_db()
            for sensor in data:
                sql = '''INSERT OR IGNORE INTO sensors
                                  (sensor_id,stations_id, param_name, param_formula, param_code,
                                   param_id)
                                  VALUES (?,?, ?, ?, ?,?)'''
                values =  (sensor['id'], sensor['stationId'], sensor['param']['paramName'],
                               sensor['param']['paramFormula'], sensor['param']['paramCode'], sensor['param']['idParam']
                               )
                self.execute_sql(conn, c, sql, values)
            conn.commit()
            c.close()
            conn.close()

    def initial_payment_getData(self):

        """Call station/findAll API  to  get all stationsID,
        next  use stationID to  call station/sensors/  get sensorsID  next call data/getData/ using sensordID and fetch data to sensors_data tabel"""

        api_url = 'https://api.gios.gov.pl/pjp-api/rest/station/findAll'
        response = api_connecting(api_url)
        data = response.json()
        ids = [station['id'] for station in data]
        api_url = 'https://api.gios.gov.pl/pjp-api/rest/station/sensors/'
        sensors_data = [requests.get(api_url + str(i)).json() for i in ids]
        ids_sensors = [s['id'] for lst in sensors_data for s in lst]
        api_url = 'https://api.gios.gov.pl/pjp-api/rest/data/getData/'
        sensors_data = [{'sensor_id': i, 'data': api_connecting(api_url + str(i)).json()} for i in ids_sensors]
        sensors_data_null = []
        for dictionary in sensors_data:
            if dictionary.get("data").get("values") is None:
                for value in dictionary["data"]["values"]:
                    if value.get("value") is None:
                        sensors_data_null.append(dictionary)
                        sensors_data.remove(dictionary)
        conn, c = self.connect_db()
        inserted_rows_count = 0
        for i in sensors_data:
            sensor_id = i['sensor_id']
            data = i['data']
            key = data['key']
            if data['values'] is not None:
                for value in data['values']:
                    date = value['date']
                    value = value['value']
                    # Only insert rows with non-null values
                    if value is not None:
                        sql = "INSERT OR IGNORE INTO sensors_data " \
                              "(sensor_id, key, date, value) VALUES (?, ?, ?, ?)"
                        values = (sensor_id, key, date, value)
                        self.execute_sql(conn, c, sql, values)
                        conn.commit()
                        inserted_rows_count += 1
        c.close()
        conn.close()
        print(f"Total rows inserted: {inserted_rows_count}")
