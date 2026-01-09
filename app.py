from cProfile import label
import city_data
from api_manager import FlightAPI


import streamlit as st
from database import DB
import plotly.graph_objects as go
db = DB()
api = FlightAPI()

st.set_page_config(layout="wide")
st.sidebar.title("Menu Section")

user_option = st.sidebar.selectbox('Menus',['Select One','Overall Analysis', 'Flight Details','Checking Availability'])
if user_option == 'Overall Analysis':    #second work on analytics and make some pie chart of airlines
    st.title("Overall Analysis")
    airline, count = db.fetching_count()
    fig=go.Figure(go.Pie(
        labels= airline,
        values= count,
        textinfo="label+value+percent",
        hoverinfo= "label+percent" ))
    st.plotly_chart(fig)
    st.header("Flight Details")




elif user_option == 'Checking Availability':
    st.title("Checking Availability")


elif user_option == 'Flight Details':        # first process on flight details
    st.title("Flight Details")

    col1,col2,col3 = st.columns(3)
    city = city_data.get_city_names()                   # fetch data from database file using db object and access function fetching_city()
    with col1:
        Sources = st.selectbox("Sources",sorted(city))
        Source_code= city_data.get_airport_code(Sources)
    with col2:
        Destination = st.selectbox("Destination",sorted(city))
        Destination_code = city_data.get_airport_code(Destination)

    with col3:
        date = st.date_input("Date")


    if st.button("Search"):
        date_str = date.strftime("%Y-%m-%d")

        st.info(f"Searching flights from {Source_code} to {Destination_code} on {date_str}...")

        try:
            result= api.search_flights(Source_code,Destination_code,date_str)
            if result.empty:
                st.warning("No flights found")
            else:
                st.success("Flights Found!")
                st.dataframe(result, hide_index=True)
        except Exception as e:
            st.error(f"An error occurred: {e}")



else:
    pass