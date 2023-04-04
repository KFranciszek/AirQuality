import pandas as pd
import stations_map
import streamlit as st
from station_info import StationInfo
from stations_map import StationsMap
#from Initial_data_load_db import DataBaseWork
import pandas
import streamlit.components.v1 as components
from unidecode import unidecode
import  matplotlib as plt

station_info = StationInfo()
stations_map = StationsMap()
#data_base_work = DataBaseWork()

st.title("Air Quality App")
st.sidebar.title("Data filtering")

# style_tabel = """
# <style>
#     .reportview-container .main {
#         max-width: 1500px;
#         padding-top: 50px;
#         padding-right: 100px;
#         padding-left: 100px;
#         padding-bottom: 50px;
#     }
# </style>
# """



def station_filtr(stations):
    station_list = [i[1] for i in stations]
    stations_id = {i[1]: i[2] for i in stations}
    selected_station = st.sidebar.selectbox("Select a station", station_list)
    if station_list:
        stations_id = stations_id[selected_station]
        sensors_mesure = station_info.sensors_list_by_station_all_db(stations_id)
        if sensors_mesure:
            parameters = [i[2] for i in sensors_mesure]
            selected_parameters = st.sidebar.selectbox("Select parametr", parameters)
            if selected_parameters:
                selected_parameter_index = parameters.index(selected_parameters)
                parameters_id = sensors_mesure[selected_parameter_index][0]
                parameters_data = station_info.sensors_data_by_sensors_db(parameters_id)
                df = pd.DataFrame(parameters_data, columns=['Kolumna 1', 'Kolumna 2', 'Kolumna 3','Kolumna 4'])
                df = df.loc[:, ['Kolumna 3', 'Kolumna 4']].rename(
                    columns={'Kolumna 3': 'Date', 'Kolumna 4': 'Value'})
                st.write("Statistical data on the selected reagent.")
                show_chart=st.line_chart(df,x="Date",y="Value")
                st.write(df)



#CITY CHOSE#
city_name = st.sidebar.text_input("Find stations in a given city")
if city_name:
    stations = station_info.station_list_by_city_user_db(city_name)
    if stations:
        st.sidebar.write("Measuring stations in the city:")
        station_filtr(stations)
    else:
        st.sidebar.write("No stations in city")

#CITY DROPDWOWN#
if not city_name:
    city_list = station_info.station_list_by_city_all_db()
    city_list = sorted([i[0] for i in city_list],key=lambda city_list: unidecode(city_list))
    city_list=st.sidebar.selectbox("Chose city:",city_list)
    if city_list and not city_name:
        stations = station_info.station_list_by_city_user_db(city_list)
        station_filtr(stations)
else:
    None

#CITY MAP#
city_map_show = st.sidebar.button("Show city map")
if city_map_show:
    # Read the content of the 'map.html' file
    with open("map.html", "r", encoding="utf-8") as file:
        map_html = file.read()
    # Display the HTML content of the map
    components.html(map_html, width=700, height=500)


#DB UPDATE#
#update_data = st.sidebar.button("Update data")
#update_data = data_base_work.initial_payment_getData()

