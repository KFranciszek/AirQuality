import requests
import json
import sqlite3


def api_connecting(api_url):
    try:
        response = requests.get(api_url)
        return  response
    except requests.exceptions.RequestException as e:
        print("An error occurred while making the request:", e)
#
# #class to call the appropriate methods
#     def api_measuring_stations(self):
#         #download a list of all measuring stations
#         api_url = 'https://api.gios.gov.pl/pjp-api/rest/station/findAll'
#         response = requests.get(api_url)
#         if response.status_code == 200:
#             data = response.json()
#             return data
#         else:
#             print(response.status_code)
#
#
#     def api_measurement_stations(self,stationId):
#         #downloading measurement stations based on station and specifically stationId
#         api_url = 'https://api.gios.gov.pl/pjp-api/rest/station/sensors/'
#         api_url  = api_url+str(stationId)
#         response = requests.get(api_url)
#
#         if response.status_code == 200:
#             data = response.json()
#             return data
#
#
#         else:
#             print(response.status_code)
#
#
#     def api_data_stations(self,sensorId):
#         api_url = 'https://api.gios.gov.pl/pjp-api/rest/data/getData/'
#         api_url  = api_url+str(sensorId)
#         response = requests.get(api_url)
#
#         if response.status_code == 200:
#             data = response.json()
#             return data
#
#
#         else:
#             print(response.status_code)
#
#     def api_air_quality_index(self, stationId):
#         api_url = 'https://api.gios.gov.pl/pjp-api/rest/aqindex/getIndex/'
#         api_url = api_url + str(stationId)
#         response = requests.get(api_url)
#
#         if response.status_code == 200:
#             data = response.json()
#             return data
#
#
#
#         else:
#             print(response.status_code)
#
#     def api_predictions(self,i,terc):
#         api_url = 'https://api.prognozy.ios.edu.pl/v1/'
#         dusts = ['PM10','NO2','SO2']
#         if i in dusts:
#             api_url = api_url+i
#         else:
#             print('dust dont exist')
#
#         api_url = api_url+"/"+str(terc)
#
#         try:
#             response = requests.get(api_url,verify=False)
#         except Exception:
#             pass
#         if response.status_code == 200:
#             data = response.json()
#             return  data
#
#
#         else:
#             print(response.status_code)
#
#
#
# class Station_info():
#     def station_list_by_city_api(self):
#         api_url = 'https://api.gios.gov.pl/pjp-api/rest/station/findAll'
#         response = requests.get(api_url)
#         if response.status_code == 200:
#             data = response.json()
#             station_names = [data['stationName'] for data in data]
#             return station_names
#
#     def  station_list_by_city_user(self,name):
#         api_url = 'https://api.gios.gov.pl/pjp-api/rest/station/findAll'
#         response = requests.get(api_url)
#         if response.status_code == 200:
#             data = response.json()
#             station_names = [{'stationName': station['stationName'], 'id': station['id']} for station in data if station['city']['name'] == name]
#
#             return station_names
#
#     def station_list_by_city_user_db(self,city_name):
#         conn = sqlite3.connect('airquality_db.db')
#         c = conn.cursor()
#         c.execute(f'''Select city_name,address_street from stations where city_name = "{city_name}"''')
#         search_result = c.fetchall()
#         conn.commit()
#         conn.close()
#         return  search_result
#
#
#     def station_list_by_city_all_db(self):
#         conn = sqlite3.connect('airquality_db.db')
#         c = conn.cursor()
#         c.execute(f'''Select Distinct(city_name) from stations''')
#         search_result = c.fetchall()
#         conn.commit()
#         conn.close()
#         return  search_result
#
#
#     def sensors_list_by_station_all_db(self,stations_id):
#         conn = sqlite3.connect('airquality_db.db')
#         c = conn.cursor()
#         c.execute(f'''Select * from sensors where stations_id = "{stations_id}"''')
#         search_result = c.fetchall()
#         conn.commit()
#         conn.close()
#         return  search_result
#
#
#
#     def sensors_data_by_sensors_db(self,sensor_id):
#         conn = sqlite3.connect('airquality_db.db')
#         c = conn.cursor()
#         c.execute(f'''Select * from sensors_data where sensor_id = "{sensor_id}"''')
#         search_result = c.fetchall()
#         conn.commit()
#         conn.close()
#         return  search_result
#
#
#
#     #join do zrobienia i wyciągnięcia (połaczenie 3 tabel)
#     def sensors_data_by_stations_db(self,stations_id):
#         conn = sqlite3.connect('airquality_db.db')
#         c = conn.cursor()
#         c.execute(f'''select * from sensors_data as sd
# inner join sensors as s on sd.sensor_id = s.sensor_id
# inner join stations as st on st.stations_id = s.stations_id
# where st.stations_id = "{stations_id}"''')
#         search_result = c.fetchall()
#         conn.commit()
#         conn.close()
#         return  search_result
#
#
#
#
#
#
#
#     def api_measurement_stations(self, stationId):
#         # downloading measurement stations based on station and specifically stationId
#         api_url = 'https://api.gios.gov.pl/pjp-api/rest/station/sensors/'
#         api_url = api_url + str(stationId)
#         response = requests.get(api_url)
#
#         if response.status_code == 200:
#             data = response.json()
#
#             return data
#
#
#         else:
#             print(response.status_code)
#
#     def api_data_stations_by_time(self,sensorId):
#         api_url = 'https://api.gios.gov.pl/pjp-api/rest/data/getData/'
#         api_url  = api_url+str(sensorId)
#         response = requests.get(api_url)
#
#         if response.status_code == 200:
#             data = response.json()
#             return data
#
#
#         else:
#             print(response.status_code)
#
#
#
# class Data_analysis():
#
#
#     def average_data_db(self,sensor_id):
#         conn = sqlite3.connect('airquality_db.db')
#         c = conn.cursor()
#         c.execute(f'''Select AVG(value) from sensors_data where sensor_id = "{sensor_id}"''')
#         search_result = c.fetchone()[0]
#         conn.commit()
#         conn.close()
#         return round(search_result,3)
#
#     def smallest_largest_data_db(self,sensor_id):
#         conn = sqlite3.connect('airquality_db.db')
#         c = conn.cursor()
#         c.execute(f'''Select max(value), min(value) from sensors_data where sensor_id = "{sensor_id}"''')
#         search_result = c.fetchone()[:]
#         conn.commit()
#         conn.close()
#         return ("Max value:", search_result[0], "Min value:", search_result[1])
#
#
#
#
#
#
# class Data_base_work():
#
#     def initial_payment_stations(self):
#         # pobranie listy wszystkich stacji pomiarowych
#         api_url = 'https://api.gios.gov.pl/pjp-api/rest/station/findAll'
#         response = requests.get(api_url)
#         if response.status_code == 200:
#             data = response.json()
#             # połączenie z bazą danych
#             conn = sqlite3.connect('airquality_db.db')
#             c = conn.cursor()
#             # wstawienie danych do tabeli
#             for station in data:
#                 city = station['city']
#                 commune = city['commune']
#                 c.execute('''INSERT INTO stations
#                              (stations_id, station_name, gegr_lat, gegr_lon, city_id,
#                               city_name, commune_name, district_name,
#                               province_name, address_street)
#                              VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
#                           (station['id'], station['stationName'], station['gegrLat'],
#                            station['gegrLon'], city['id'], city['name'],
#                            commune['communeName'], commune['districtName'],
#                            commune['provinceName'], station['addressStreet']))
#             # zatwierdzenie zmian i zamknięcie połączenia
#             conn.commit()
#             conn.close()
#
#         else:
#             print(response.status_code)
#
#     def initial_payment_sensors(self):
#         # pobranie listy wszystkich stacji pomiarowych
#         api_url = 'https://api.gios.gov.pl/pjp-api/rest/station/findAll'
#         response = requests.get(api_url)
#         if response.status_code == 200:
#             data = response.json()
#             ids = [station['id'] for station in data]
#             sensors_data = []
#             for i in ids:
#                 api_url = 'https://api.gios.gov.pl/pjp-api/rest/station/sensors/'
#                 api_url = api_url + str(i)
#                 response = requests.get(api_url)
#                 if response.status_code == 200:
#                     data = response.json()
#                     sensors_data.append(data)
#                     conn = sqlite3.connect('airquality_db.db')
#                     c = conn.cursor()
#
#                     for sensor in data:
#                         c.execute('''INSERT INTO sensors
#                                      (sensor_id,stations_id, param_name, param_formula, param_code,
#                                       param_id)
#                                      VALUES (?,?, ?, ?, ?,?)''',
#                                   (sensor['id'],sensor['stationId'], sensor['param']['paramName'],
#                                    sensor['param']['paramFormula'], sensor['param']['paramCode'], sensor['param']['idParam']
#                                    ))
#                     conn.commit()
#                     conn.close()
#                 else:
#                     print(response.status_code)
#         else:
#             print(response.status_code)
#
#     def initial_payment_getData(self):
#         api_url = 'https://api.gios.gov.pl/pjp-api/rest/station/findAll'
#         response = requests.get(api_url)
#         if response.status_code == 200:
#             data = response.json()
#             ids = [station['id'] for station in data]
#             api_url = 'https://api.gios.gov.pl/pjp-api/rest/station/sensors/'
#             sensors_data = [requests.get(api_url + str(i)).json() for i in ids]
#             ids_sensors = [s['id'] for lst in sensors_data for s in lst]
#             api_url = 'https://api.gios.gov.pl/pjp-api/rest/data/getData/'
#             sensors_data = [{'sensor_id':i,'data':requests.get(api_url + str(i)).json()} for i in ids_sensors]
#             conn = sqlite3.connect('airquality_db.db')
#             c = conn.cursor()
#             for i in sensors_data:
#                 sensor_id = i['sensor_id']
#                 data = i['data']
#                 key = data['key']
#                 for value in data['values']:
#                     date = value['date']
#                     value = value['value']
#                     c.execute("INSERT INTO sensors_data (sensor_id, key,date, value) VALUES (?, ?, ?,?)",
#                               (sensor_id, key,date, value))
#                     conn.commit()
#             conn.close()




            #return  get_data_sensors

            #return  ids
            #for i in ids:
               # api_url = 'https://api.gios.gov.pl/pjp-api/rest/station/sensors/'
               # api_url = api_url + str(i)

            #    response = requests.get(api_url)
                #if response.st atus_code == 200:
                 #   data = response.json()
                 #   sensors_data.append(i)







#
# station_info = Station_info()
# station_info = Station_info()
# data_info = station_info.sensors_data_by_stations_db(114)
# print(data_info)



#api_connect =  Api_Connect()
#find_all=api_connect.api_measuring_stations()
#print(find_all)
