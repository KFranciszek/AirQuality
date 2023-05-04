
import sqlite3
import folium
import geopy
from geopy import geocoders
from geopy.geocoders import Nominatim
from geopy.distance import  geodesic

from Initial_data_load_db import DataBaseWork

data_base_work = DataBaseWork()

class StationsMap():

    """

    A class that groups together methods related to displaying
    a map and calculating the distance from a given point and, based on that,
    pulling up the nearest stations. The class uses the bilibrary of folium and geopy

    """

    def show_station_on_map(self):

        """

        The method extracts the bearings of all stations from the base and,
        using the folium library, creates a map by placing pins at the station location.

        """

        sql = 'SELECT station_name,gegr_lat,gegr_lon from stations'
        search_result=data_base_work.db_operations(sql)
        return search_result
        latitude, longitude = float(search_result[0][1]), float(search_result[0][2])
        zoom_level = 6  # Adjust the zoom level according to your preference
        map = folium.Map(location=(latitude, longitude), zoom_start=zoom_level)
        for point in search_result:
            name,lat,lon = point
            lat,lon = float(lat),float(lon)
            marker = folium.Marker(location=(lat, lon), popup=name)
            marker.add_to(map)
        map.save('map.html')

    def show_station_on_map_by_distance(self, location,distance_point):

        """

            A method that, based on a given point on the map and a range of kilometers,
            shows stations within that range

        """

        try:
            geolocator = Nominatim(user_agent="myGeocoder")
            location_check=geolocator.geocode(location)
            location_check=(location_check.latitude, location_check.longitude)
        except (ValueError,AttributeError) as e:
            print(f"Invalid error: {e}")
        sql = 'SELECT gegr_lat,gegr_lon,station_name,stations_id,city_name from stations'
        search_result=data_base_work.db_operations(sql)
        try:
            point1 = location_check
            locations = []
            for i in search_result:
                point2 = (i[0],i[1])
                distance = geodesic(point1,point2)
                locations.append(distance.kilometers)
            result_km  =[]
            for index, x in enumerate(locations):
                if x <= distance_point:
                    result_km.append(search_result[index][2:5])
        except TypeError as te:
            print(f"Invalid error: {te}")
        return result_km
