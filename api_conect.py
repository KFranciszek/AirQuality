import requests
import json
class Api_Connect():
#class to call the appropriate methods
    def api_measuring_stations(self):
        #download a list of all measuring stations
        api_url = 'https://api.gios.gov.pl/pjp-api/rest/station/findAll'
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(response.status_code)


    def api_measurement_stations(self,stationId):
        #downloading measurement stations based on station and specifically stationId
        api_url = 'https://api.gios.gov.pl/pjp-api/rest/station/sensors/'
        api_url  = api_url+str(stationId)
        response = requests.get(api_url)

        if response.status_code == 200:
            data = response.json()
            return data


        else:
            print(response.status_code)


    def api_data_stations(self,sensorId):
        api_url = 'https://api.gios.gov.pl/pjp-api/rest/data/getData/'
        api_url  = api_url+str(sensorId)
        response = requests.get(api_url)

        if response.status_code == 200:
            data = response.json()
            return data


        else:
            print(response.status_code)

    def api_air_quality_index(self, stationId):
        api_url = 'https://api.gios.gov.pl/pjp-api/rest/aqindex/getIndex/'
        api_url = api_url + str(stationId)
        response = requests.get(api_url)

        if response.status_code == 200:
            data = response.json()
            return data



        else:
            print(response.status_code)

    def api_predictions(self,i,terc):
        api_url = 'https://api.prognozy.ios.edu.pl/v1/'
        dusts = ['PM10','NO2','SO2']
        if i in dusts:
            api_url = api_url+i
        else:
            print('dust dont exist')

        api_url = api_url+"/"+str(terc)

        try:
            response = requests.get(api_url,verify=False)
        except Exception:
            pass
        if response.status_code == 200:
            data = response.json()
            return  data


        else:
            print(response.status_code)



class Station_info():
    def station_list_by_city(self):
        api_url = 'https://api.gios.gov.pl/pjp-api/rest/station/findAll'
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            station_names = [data['stationName'] for data in data]
            return station_names

    def  station_list_by_city_user(self,name):
        api_url = 'https://api.gios.gov.pl/pjp-api/rest/station/findAll'
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            station_names = [{'stationName': station['stationName'], 'id': station['id']} for station in data if station['city']['name'] == name]

            return station_names

    def api_measurement_stations(self, stationId):
        # downloading measurement stations based on station and specifically stationId
        api_url = 'https://api.gios.gov.pl/pjp-api/rest/station/sensors/'
        api_url = api_url + str(stationId)
        response = requests.get(api_url)

        if response.status_code == 200:
            data = response.json()
            return data


        else:
            print(response.status_code)

    def api_data_stations(self,sensorId):
        api_url = 'https://api.gios.gov.pl/pjp-api/rest/data/getData/'
        api_url  = api_url+str(sensorId)
        response = requests.get(api_url)

        if response.status_code == 200:
            data = response.json()
            return data


        else:
            print(response.status_code)


class data_base_work():
    def initial_payment(self):


    def check_measuring_stations_sensors(self):


    def save_data_air(self):





station_info = Station_info()
all_stations = station_info.station_list_by_city_user("Wrocław")
print(all_stations)



#api_connect =  Api_Connect()
#find_all=api_connect.api_measuring_stations()
#print(find_all)
