import pandas as pd
import stations_map
import streamlit as st
from station_info import StationInfo
from stations_map import StationsMap
import pandas
import streamlit.components.v1 as components

station_info = StationInfo()
stations_map = StationsMap()

st.title("Air Quality App")
st.sidebar.title("Data filtering")
city_name = st.sidebar.text_input("Find stations in a given city")
city_list = station_info.station_list_by_city_all_db()
ciity_name_list =st.sidebar.selectbox("Chose city:",city_list)
city_map_show = st.sidebar.button("Show city map")
if city_map_show:
    # Read the content of the 'map.html' file
    with open("map.html", "r", encoding="utf-8") as file:
        map_html = file.read()

    # Display the HTML content of the map
    components.html(map_html, width=700, height=500)

if city_name:
    stations = station_info.station_list_by_city_user_db(city_name)
    #def city_tape():
    if stations:
       st.sidebar.write("Measuring stations in the city:")
       station_list=[i[1] for i in stations]
       stations_id ={i[1]: i[2]for i in stations}
       #st.write(stations_id)
       selected_station = st.sidebar.selectbox("Select a station", station_list)
       if station_list:
           stations_id = stations_id[selected_station]
           sensors_mesure = station_info.sensors_list_by_station_all_db(stations_id)
           if sensors_mesure:
               parameters = [i[2] for i in sensors_mesure]
               selected_parameters = st.sidebar.selectbox("Select parametr",parameters)
               if selected_parameters:
                   #button_all=st.sidebar.button("Show all data in sensor")
                   #button_all = station_info.sensors_data_by_stations_db(stations_id)
                   #st.write(button_all)
                   selected_parameter_index = parameters.index(selected_parameters)
                   parameters_id = sensors_mesure[selected_parameter_index][0]
                   parameters_data = station_info.sensors_data_by_sensors_db(parameters_id)
                   df = pd.DataFrame(parameters_data)
                   st.write(df)




    else:
        st.sidebar.write("No stations in city")


#if ciity_name_list:
#    city_tape()