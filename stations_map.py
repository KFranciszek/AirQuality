
import sqlite3
import folium
import geopy
from geopy import geocoders
from geopy.geocoders import Nominatim
from geopy.distance import  geodesic



class StationsMap():
    def show_station_on_map(self):
        try:
            conn = sqlite3.connect('airquality_db_test2.db.db')
            c = conn.cursor()
            c.execute(f'''SELECT station_name,gegr_lat,gegr_lon from stations''')
            search_result = c.fetchall()
            conn.commit()
            c.close()
            conn.close()
        except sqlite3.Error as e:
            print("An error occurred while connecting to the database:", e)

        latitude, longitude = float(search_result[0][1]), float(search_result[0][2])
        zoom_level = 10  # Adjust the zoom level according to your preference
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

        try:
            conn = sqlite3.connect('airquality_db_test2.db')
            c = conn.cursor()
            c.execute(f'''SELECT gegr_lat,gegr_lon,station_name,stations_id,city_name from stations''')
            search_result = c.fetchall()
            conn.commit()
            c.close()
            conn.close()
        except (sqlite3.OperationalError, sqlite3.Error,) as e:
            print("db error:", e)

        try:
            point1 = location_check
            locations = []
            for i in search_result:
                point2 = (i[0],i[1])
                distance = geodesic(point1,point2)
                #print(distance)
                locations.append(distance.kilometers)

            result_km  =[]
            for index, x in enumerate(locations):
                if x <= distance_point:
                    result_km.append(search_result[index][2:5])


        except TypeError as te:
            print(f"Invalid error: {te}")
        return result_km
