import streamlit as st
from ai_scraper import getTrip
from format_flights import formatFlights
import pandas as pd

ss = st.session_state

st.set_page_config(layout="wide")

if 'travelData' not in ss:
    ss.travelData = []
if 'filteredTrips' not in ss:
    ss.filteredTrips = []

st.title('trip finder')

def formatData(source):
    sourceDataA = {
        'sourceAirport': f'{source}',
        'trips': []
    }
    tripDetails = getTrip()
    sourceDataA['trips'].append(
            {
                'dates': f"Dec {1} - Dec {6}",
                "details": tripDetails
            }
        )
    ss.travelData.append(sourceDataA) 

col1, col2 = st.columns([1, 1])
with col1:
    st.text_input('Source Airport 1', 'JFK', disabled=True)
    start_date = st.date_input('Possible start date', pd.to_datetime('2024-12-01'), disabled=True)
    end_date = st.date_input('Possible end date', pd.to_datetime('2024-12-08'), disabled=True)
    st.text_input('Duration', '5', disabled=True)
    if st.button('get trips'):
        if len(ss.travelData) == 0:
            formatData("JFK")
            # formatData("LAX")
            # formatData("ORD")
            # formatData("DFW")
            # formatData("DEN")
            # formatData("SFO")

with col2:
    dates = ['Dec 1 - Dec 6']
    if st.button('show trips'): 
        for trip in ss.travelData[0]["trips"][0]["details"]:
            with st.expander(f"Go to {trip['flight_location']} from {dates[0]}"):
                st.write(f"Total price: ${trip['flight_price']}")