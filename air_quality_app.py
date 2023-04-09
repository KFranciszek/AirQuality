import pandas as pd
import stations_map
import streamlit as st
from station_info import StationInfo
from stations_map import StationsMap
from Initial_data_load_db import DataBaseWork
import pandas
import streamlit.components.v1 as components
from unidecode import unidecode
import  matplotlib as plt
import datetime

station_info = StationInfo()
stations_map = StationsMap()
data_base_work = DataBaseWork()
st.set_page_config(layout="wide")
st.title("Air Quality App")
main_container = st.container()
col1, col2 = main_container.columns([1, 1])

with st.sidebar:
    st.sidebar.title("Data filtering")


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
                date_range_list = (3, 7, 14, 30, 60, 90, 180, 365)
                date_range = st.sidebar.selectbox("Chose date raneg", date_range_list)
                current_date = pd.Timestamp.now()
                delta = pd.Timedelta(days=date_range)
                result_date = current_date - delta
                result_date_str = result_date.strftime('%Y-%m-%d %H:%M:%S')
                try:
                    df=df.loc[df['Date'] > result_date_str]
                    with col1:
                        st.write("Tabel data.")
                        st.dataframe(df,width=500, height=800)
                    with col2:
                        st.write("Charts and mapa data.")
                        average_value = df['Value'].mean()
                        max_value_index =df['Value'].idxmax()
                        min_value_index =df['Value'].idxmin()
                        # Get the max and min values
                        max_value = df.loc[max_value_index, 'Value']
                        min_value = df.loc[min_value_index, 'Value']
                        # Get the corresponding dates for the max and min values
                        max_date = df.loc[max_value_index, 'Date']
                        min_date = df.loc[min_value_index, 'Date']
                        #Formating data analys
                        avg_string = f"Average value is: {average_value:.2f}"
                        max_string =  f"Maxium value: {max_value:.2f} at {max_date} "
                        min_string  =f"Minimum value: {min_value:.2f} at {min_date} "
                        st.write(avg_string,"-",max_string,"-",min_string)
                        show_chart=st.line_chart(df,x="Date",y="Value")
                except ValueError as ve:
                 print("Error:", ve)






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
    with col2:
        components.html(map_html, width=700, height=500)

#Update data butto-def and downolad it#
update_button= st.sidebar.button("Update data")

if update_button:
    data_base_work.initial_payment_getData()
    st.sidebar.success("Data updated successfully!")






