import streamlit as st
from ai_scraper import getTrip
import pandas as pd
from ai_scraper import test

ss = st.session_state

st.set_page_config(layout="wide")

if 'travelData' not in ss:
    ss.travelData = []
if 'filteredTrips' not in ss:
    ss.filteredTrips = []

st.title('trip finder')

col1, col2 = st.columns([1, 1])
with col1:
    st.text_input('Source Airports', 'JFK, AUS, ORD', disabled=True)
    start_date = st.date_input('Possible start date', pd.to_datetime('2024-12-01'), disabled=True)
    end_date = st.date_input('Possible end date', pd.to_datetime('2024-12-07'), disabled=True)
    st.text_input('Duration', '5', disabled=True)
    if st.button('get trips'):
        ss.travelData = test()

with col2:
    if st.button('show trips'): 
        for trip in ss.travelData:
            with st.expander(f"${trip['total_price']} : Go to {trip['destination']} from {trip['start_date']} to {trip['end_date']}"):
                for trip in trip['trips']:
                    st.write(f"{trip['price']} from {trip['source']} : {trip['duration']} and {trip['number_of_stops']}")