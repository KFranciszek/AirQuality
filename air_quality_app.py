#Module for framework Streamlit#


import streamlit as st
import streamlit.components.v1 as components

from unidecode import unidecode
import pandas as pd
import numpy as np

from config import date_range_list,km_list
from station_info import StationInfo
from stations_map import StationsMap
from Initial_data_load_db import DataBaseWork


station_info = StationInfo()
stations_map = StationsMap()
data_base_work = DataBaseWork()

#App layouts#
st.set_page_config(layout="wide")
st.title("Air Quality App")
main_container = st.container()
col1, col2 = main_container.columns([1, 1])
col3, col4, col5 = st.sidebar.columns(3)
with st.sidebar:
    st.sidebar.title("Data filtering")
    radio_value=st.sidebar.radio("Chose how find data",
                                 ["City list", "Search city", "Distance point"])

def sensor_filtr(sensors_mesure):
    if sensors_mesure:
        parameters = [i[2] for i in sensors_mesure]
        selected_parameters = st.sidebar.selectbox("Select parametr", parameters)
        if selected_parameters:
            selected_parameter_index = parameters.index(selected_parameters)
            parameters_id = sensors_mesure[selected_parameter_index][0]
            parameters_data = station_info.sensors_data_by_sensors_db(parameters_id)
            if len(parameters_data) == 0:
                st.sidebar.write("Not data for this sensor")
            else:
                df = pd.DataFrame(parameters_data,
                                  columns=['Kolumna 1', 'Kolumna 2', 'Kolumna 3', 'Kolumna 4'])
                df = df.loc[:, ['Kolumna 3', 'Kolumna 4']].rename(
                    columns={'Kolumna 3': 'Date', 'Kolumna 4': 'Value'})
                date_range = st.sidebar.selectbox("Choose date range", date_range_list)
                current_date = pd.Timestamp.now()
                delta = pd.Timedelta(days=date_range)
                result_date = current_date - delta
                result_date_str = result_date.strftime('%Y-%m-%d %H:%M:%S')
                try:
                    df = df.loc[df['Date'] > result_date_str]
                    if df.empty:
                        st.sidebar.write("In this timeframe, no data is available")
                    else:

                        with col1:
                            st.write("Table data.")
                            st.dataframe(df, width=500, height=800)
                        with col2:
                            st.write("Charts and map data.")
                            average_value = df['Value'].mean()
                            max_value_index = df['Value'].idxmax()
                            min_value_index = df['Value'].idxmin()
                            # Get the max and min values
                            max_value = df.loc[max_value_index, 'Value']
                            min_value = df.loc[min_value_index, 'Value']
                            # Get the corresponding dates for the max and min values
                            max_date = df.loc[max_value_index, 'Date']
                            min_date = df.loc[min_value_index, 'Date']
                            # Formating data analys
                            avg_string = f"Average value is: {average_value:.2f}"
                            max_string = f"Maxium value: {max_value:.2f} at {max_date} "
                            min_string = f"Minimum value: {min_value:.2f} at {min_date} "
                            st.write(avg_string, "-", max_string, "-", min_string)
                            x = np.arange(len(df))
                            y = df["Value"]
                            coefficients = np.polyfit(x, y, 1)
                            trend_line = np.poly1d(coefficients)
                            df["Trend"] = trend_line(x)
                            show_chart=st.line_chart(df.set_index("Date"))
                        with col5:
                            csv = df.to_csv()
                            dowland_csv = col5.download_button(label="Download data CSV",
                                                               data=csv, file_name='large_df.csv',
                                                               mime='text/csv', )
                except (ValueError, TypeError) as error:
                        print("Error:", error)

def station_filtr(stations):
    station_list = [i[1] for i in stations]
    stations_id = {i[1]: i[2] for i in stations}
    selected_station = st.sidebar.selectbox("Select a station", station_list)
    if station_list:
        stations_id = stations_id[selected_station]
        sensors_mesure = station_info.sensors_list_by_station_all_db(stations_id)
        sensor_filtr(sensors_mesure)

#City choose#
if radio_value == "Search city":
    city_name = st.sidebar.text_input("Find stations in the given city")
    stations = station_info.station_list_by_city_user_db(city_name)
    if stations:
        st.sidebar.write("Measuring stations in the city:")
        station_filtr(stations)
    else:
        if city_name == "":
            pass
        else:
            st.sidebar.write("City doesn't appear")

#City dropdown#
if radio_value == "City list":
    city_list = station_info.station_list_by_city_all_db()
    city_list = sorted([i[0] for i in city_list],key=lambda city_list: unidecode(city_list))
    city_list=st.sidebar.selectbox("Choose city:",city_list)
    if city_list  and radio_value == "City list":
        stations = station_info.station_list_by_city_user_db(city_list)
        station_filtr(stations)
else:
    pass

#City by distance#
if radio_value == "Distance point":
    point_chose = st.sidebar.text_input("Find stations in the given point")
    km = st.sidebar.selectbox("Km + ", km_list)
    try:
        station_list_point = stations_map.show_station_on_map_by_distance(point_chose, km)
        station_list_point_list = {i[0]:i[1] for i in station_list_point}
        select_point_stations = st.sidebar.selectbox("Select a station by distance point",
                                                     station_list_point_list)
        stations_id = station_list_point_list[select_point_stations]
        sensors_mesure = station_info.sensors_list_by_station_all_db(stations_id)
        sensor_filtr(sensors_mesure)
    except (ValueError, TypeError,KeyError) as error:
     print("Error:", error)


#City map#
with open("map.html", "r", encoding="utf-8") as file:
    map_html = file.read()
with col2:
    components.html(map_html, width=700, height=500)

#Add a button to each column#
update_button = col4.button("Update data")
show_map_button = col3.button('Show data on map')
#Update data button-def#
if update_button:
    data_base_work.initial_payment_getData()
    st.sidebar.success("Data updated successfully!")
