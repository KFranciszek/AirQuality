
import sqlite3
import folium


class StationsMap():
    def show_station_on_map(self):
        try:
            conn = sqlite3.connect('airquality_db.db')
            c = conn.cursor()
            c.execute(f'''SELECT station_name,gegr_lat,gegr_lon from stations''')
            search_result = c.fetchall()
            conn.commit()
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



stations_map = StationsMap()
stations_map.show_station_on_map()
