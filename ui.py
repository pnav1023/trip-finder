import streamlit as st
from scraper import getTrip, testScraper
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
    for i in range(3):
        tripDetails = getTrip(i, source)
        sourceDataA['trips'].append(
                {
                    'dates': f"Dec {i+1} - Dec {i+6}",
                    "details": tripDetails
                }
            )
    ss.travelData.append(sourceDataA) 

col1, col2 = st.columns([1, 1])
with col1:
    st.text_input('Source Airport 1', 'AUS', disabled=True)
    st.text_input('Source Airport 2', 'JFK', disabled=True)
    start_date = st.date_input('Possible start date', pd.to_datetime('2024-12-01'), disabled=True)
    end_date = st.date_input('Possible end date', pd.to_datetime('2024-12-08'), disabled=True)
    st.text_input('Duration', '5', disabled=True)
    if st.button('get trips'):
        if len(ss.travelData) == 0:
            formatData("AUS") 
            formatData("JFK")
            # formatData("LAX")
            # formatData("ORD")
            # formatData("DFW")
            # formatData("DEN")
            # formatData("SFO")

with col2:
    dates = ['Dec 1 - Dec 6', 'Dec 2 - Dec 7', 'Dec 3 - Dec 8']
    if st.button('show trips'): 
        ss.filteredTrips = formatFlights(ss.travelData)
        for trip in ss.filteredTrips:
            with st.expander(f"Go to {trip['destination']} from {trip['dates']}"):
                st.write(f"Total price: ${trip['total_price']}")
                for trip_detail in trip['trips']:
                    st.write(f"Flights from {trip_detail['source']} to {trip['destination']} start at ${trip_detail['price']}")
    