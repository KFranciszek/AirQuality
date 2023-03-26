#Module that returns various values and conversions directly from the API of the air quality institute

import requests
import json

class ApiConnect():

#Return all station name from API
    def station_list_by_city_api(self):
        try:
            api_url = 'https://api.gios.gov.pl/pjp-api/rest/station/findAll'
            response = requests.get(api_url)
            if response.status_code == 200:
                data = response.json()
                station_names = [data['stationName'] for data in data]
                return station_names
        except requests.exceptions.RequestException as e:
            print("An error occurred while making the request:", e)
        except requests.exceptions.HTTPError as e:
            print("The server returned a bad status code:", e)
        except requests.exceptions.Timeout as e:
            print("The request timed out:", e)

#Return all station name and id from API by  city name type by user
    def  station_list_by_city_user(self,name):
        try:
            api_url = 'https://api.gios.gov.pl/pjp-api/rest/station/findAll'
            response = requests.get(api_url)
            if response.status_code == 200:
                data = response.json()
                station_names = [{'stationName': station['stationName'], 'id': station['id']} for station in data if station['city']['name'] == name]
                return station_names
        except requests.exceptions.RequestException as e:
            print("An error occurred while making the request:", e)
        except requests.exceptions.HTTPError as e:
            print("The server returned a bad status code:", e)
        except requests.exceptions.Timeout as e:
            print("The request timed out:", e)

#Downloading measurement stations based on station and specifically stationId
    def api_measurement_stations(self, stationId):
        try:
            api_url = 'https://api.gios.gov.pl/pjp-api/rest/station/sensors/'
            api_url = api_url + str(stationId)
            response = requests.get(api_url)
            data = response.json()
            return data
        except requests.exceptions.RequestException as e:
            print("An error occurred while making the request:", e)
        except requests.exceptions.HTTPError as e:
            print("The server returned a bad status code:", e)
        except requests.exceptions.Timeout as e:
            print("The request timed out:", e)

#Downloading data air quality by sensor id  from APO
    def api_data_stations_by_senorid(self,sensorId):
        try:
            api_url = 'https://api.gios.gov.pl/pjp-api/rest/data/getData/'
            api_url  = api_url+str(sensorId)
            response = requests.get(api_url)
            data = response.json()
            return data
        except requests.exceptions.RequestException as e:
            print("An error occurred while making the request:", e)
        except requests.exceptions.HTTPError as e:
            print("The server returned a bad status code:", e)
        except requests.exceptions.Timeout as e:
            print("The request timed out:", e)


    def average_data_api(self,sensorId):
        try:
            api_url = 'https://api.gios.gov.pl/pjp-api/rest/data/getData/'
            api_url = api_url + str(sensorId)
            response = requests.get(api_url)
            data = response.json()
        except requests.exceptions.RequestException as e:
            print("An error occurred while making the request:", e)
        # wybieramy pola 'value' z listy słowników
        values = [d['value'] for d in data['values']]
        average = round(sum(values) / len(values),3)
        return  average

    def smallest_largest_data_api(self,sensorId):
        try:
            api_url = 'https://api.gios.gov.pl/pjp-api/rest/data/getData/'
            api_url  = api_url+str(sensorId)
            response = requests.get(api_url)
            data = response.json()
        except requests.exceptions.RequestException as e:
            print("An error occurred while making the request:", e)

        # wybieramy pola 'value' z listy słowników
        values = [d['value'] for d in data['values']]

        # znajdujemy największą i najmniejszą wartość w polu 'value'
        max_value = max(values)
        min_value = min(values)

        # znajdujemy datę, dla której wystąpiła największa i najmniejsza wartość
        max_date = [d['date'] for d in data['values'] if d['value'] == max_value][0]
        min_date = [d['date'] for d in data['values'] if d['value'] == min_value][0]
        return [{"maxDate":max_date,"maxValue":max_value},{"minDate":min_date,"minValue":min_value}]


