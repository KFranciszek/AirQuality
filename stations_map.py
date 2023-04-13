
import sqlite3
import folium
import geopy
from geopy import geocoders
from geopy.geocoders import Nominatim
from geopy.distance import  geodesic

from Initial_data_load_db import DataBaseWork


class StationsMap():
    def show_station_on_map(self):
        data_base_work = DataBaseWork()
        conn, c = data_base_work.connect_db()
        sql = 'SELECT station_name,gegr_lat,gegr_lon from stations'
        data_base_work.execute_sql(conn, c, sql)
        search_result = c.fetchall()
        conn.commit()
        conn.close()
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
        try:
            geolocator = Nominatim(user_agent="myGeocoder")
            location_check=geolocator.geocode(location)
            location_check=(location_check.latitude, location_check.longitude)
        except (ValueError,AttributeError) as e:
            print(f"Invalid error: {e}")
        data_base_work = DataBaseWork()
        conn, c = data_base_work.connect_db()
        sql = 'SELECT gegr_lat,gegr_lon,station_name,stations_id,city_name from stations'
        data_base_work.execute_sql(conn, c, sql)
        search_result = c.fetchall()
        conn.commit()
        conn.close()
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
