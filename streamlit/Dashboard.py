import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pymongo import MongoClient
from bson.decimal128 import Decimal128
from decimal import Decimal
import toml 
st.set_page_config(
    page_title="Flights Dashboard",
    page_icon="✈️",
    layout="wide",
    #initial_sidebar_state="expanded",
)




# with open("mongo_srv.txt", "r") as file:
#     mongo_srv = file.readline().strip()

@st.fragment
def connect_to_mongo():
    client = MongoClient("mongodb+srv://reporting:ChNNKat9xpZpPOYg@cluster0.z4sob.mongodb.net/")
    db = client.kpi_graph
    return db
db = connect_to_mongo()

@st.fragment
def convert_to_dataframe(collection):
    data = list(collection.find())
    for record in data:
        for key, value in record.items():
            if isinstance(value, Decimal128):
                record[key] = Decimal(value.to_decimal())
            elif isinstance(value, Decimal):
                record[key] = float(value)
    return pd.DataFrame(data)

total_flights_per_period_col = db.total_flights_per_week
delayed_flights_per_week_col = db.delayed_flights_per_week
average_delay_time_col = db.average_delay_time_per_week
flights_over_time_col = db.flights_over_time
top_airports_by_departures_col = db.top_airports_by_departures
average_passengers_per_flight_per_week_col = db.average_passengers_per_flight_per_week
last_weeks_revenue_col = db.last_weeks_revenue
flights_lines_col = db.flights_lines


total_flights_per_period_df = convert_to_dataframe(total_flights_per_period_col)
delayed_flights_per_week_df = convert_to_dataframe(delayed_flights_per_week_col)
average_delay_time_df = convert_to_dataframe(average_delay_time_col)
#st.dataframe(average_delay_time_df)
flights_over_time_df = convert_to_dataframe(flights_over_time_col)
top_airports_by_departures_df = convert_to_dataframe(top_airports_by_departures_col)
average_passengers_per_flight_per_week_df = convert_to_dataframe(average_passengers_per_flight_per_week_col)
last_weeks_revenue_df = convert_to_dataframe(last_weeks_revenue_col)
flights_lines_df = convert_to_dataframe(flights_lines_col)

flights_over_time_df["day"] = pd.to_datetime(flights_over_time_df["day"])
flights_over_time_df["num_flights"] = flights_over_time_df["num_flights"].astype(int)


# Titre du tableau de bord
st.title("Flights Dashboard")

# En-tête des KPIs


col_1, col_2, col_3, col_4, col_5 = st.columns(5)


with col_1:
    num_flights_last_week = int(total_flights_per_period_df.iloc[0]["total_flights"]) 
    num_flights_last_2week = int(total_flights_per_period_df.iloc[1]["total_flights"])
    delta = num_flights_last_week - num_flights_last_2week
    st.metric("Total Flights", value= num_flights_last_week, delta=delta )
    
with col_2:
    num_delayed_flights_last_week = int(delayed_flights_per_week_df.iloc[0]["delayed_flights"])
    num_delayed_flights_last_2week = int(delayed_flights_per_week_df.iloc[1]["delayed_flights"])
    delta = num_delayed_flights_last_week - num_delayed_flights_last_2week
    st.metric("Delayed Flights", value=num_delayed_flights_last_week, delta=delta)
with col_3:
    avg_delay_time_last_week = round(float(average_delay_time_df.iloc[0]["average_delay_minutes"]), 2)
    avg_delay_time_last_2week = round(float(average_delay_time_df.iloc[1]["average_delay_minutes"]), 2)
    delta = round(avg_delay_time_last_week - avg_delay_time_last_2week, 2)
    st.metric("Average Delay Time", value=avg_delay_time_last_week, delta=delta)
with col_4:
    avarage_delay_time_last_week = round(float(average_passengers_per_flight_per_week_df.iloc[0]["average_passengers"]), 2)
    avarage_delay_time_last_2week = round(float(average_passengers_per_flight_per_week_df.iloc[1]["average_passengers"]), 2)
    delta = round(avarage_delay_time_last_week - avarage_delay_time_last_2week, 2)
    st.metric("Average Passengers per Flight", value=avarage_delay_time_last_week, delta=delta)
with col_5:
    last_week_revenue = round(float(last_weeks_revenue_df.iloc[0]["total_revenue"])/1000000, 2)
    last_week_revenue_last_week_str = f"{round(float(last_weeks_revenue_df.iloc[0]['total_revenue']), 2)} $B"
    last_2week_revenue = round(float(last_weeks_revenue_df.iloc[1]["total_revenue"]), 2)
    delta = round((last_week_revenue - last_2week_revenue)/1000000, 2)
    st.metric("Last Week Revenue", value=last_week_revenue_last_week_str, delta=delta)
    
# Ligne 2 :  Graphiques
col1 = st.columns(1)[0]
#st.dataframe(flights_over_time_df)
data = flights_over_time_df.sort_values(by="day", ascending=True)
daily_flights_fig = px.line(data, x="day", y="num_flights", title="Daily Flights", labels={"num_flights": "Number of Flights", "day": "Day"})
daily_flights_fig.update_traces(line=dict(color="blue"))
daily_flights_fig.update_layout(
    xaxis = dict(
        title = "Date",
    ),
    yaxis = dict(
        title = "Number of Flights",
    ),
    
)
st.plotly_chart(daily_flights_fig, use_container_width=True)

# Top aéroports par nombre de départs et relation entre distance et nombre de vols
col1, col2 = st.columns(2)

with col1:
    data = top_airports_by_departures_df.sort_values(by="num_departures", ascending=True)
    data["airport_name"] = data["airport_name"].apply(eval)
    #st.dataframe(data)
    data["name"] = data["airport_name"].apply(lambda x: x["en"])
    bar_chart = px.bar(data,
                       x="num_departures", y="name", 
                       orientation="h", title="Top Airports by Departures", 
                       labels={"num_departures": "Number of Departures", "name": "Airport Name"})
    st.plotly_chart(bar_chart, use_container_width=True)
    
with col2:
    # Convertir les données de la collection MongoDB en DataFrame pandas
    flight_list = list(flights_lines_col.find())
    flight_df = pd.DataFrame(flight_list)

    # Afficher le DataFrame avec Streamlit
    #st.write(flight_df)
    lines = []
    markers = []

    for flight in flight_list:
        # Extraire les données
        departure_coords = tuple(map(float, flight["departure_coordinates"][1:-1].split(",")))
        arrival_coords = tuple(map(float, flight["arrival_coordinates"][1:-1].split(",")))
        departure_city = eval(flight["departure_city"])["en"]
        arrival_city = eval(flight["arrival_city"])["en"]
        # Ajouter les lignes
        lines.append(
            go.Scattergeo(
                lon = [departure_coords[0], arrival_coords[0]],
                lat = [departure_coords[1], arrival_coords[1]],
                mode = "lines",
                line = dict(width = 1, color = "red"),
                opacity = 0.5
            )
        )
        # Ajouter les marqueurs pour les aéroports de départ et d'arrivée
        # Départ en bleu
        markers.append(
            go.Scattergeo(
                lon = [departure_coords[0]],
                lat = [departure_coords[1]],
                mode = "markers",
                marker = dict(size = 10, color = "blue"),
                text = departure_city,
            )
        )
        # Arrivée en rouge
        markers.append(
            go.Scattergeo(
                lon = [arrival_coords[0]],
                lat = [arrival_coords[1]],
                mode = "markers",
                marker = dict(size = 10, color = "red"),
                text = arrival_city,
            )
        )

    # Afficher les lignes et les marqueurs sur une carte
    fig = go.Figure(data=lines + markers)
    fig.update_layout(
        title="Flight Paths",
        showlegend=False,
        geo=dict(
            projection_type="equirectangular",
            showland=True,
            landcolor="rgb(243, 243, 243)",
            subunitwidth=1,
            countrywidth=1,
            subunitcolor="rgb(217, 217, 217)",
            countrycolor="rgb(217, 217, 217)"
        ),
    )
    st.plotly_chart(fig, use_container_width=True)