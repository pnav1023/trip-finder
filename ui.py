import streamlit as st
from scraper import getTrip, testScraper
import pandas as pd

ss = st.session_state

st.set_page_config(layout="wide")

if 'travelData' not in ss:
    ss.travelData = []
if 'filteredTrips' not in ss:
    ss.filteredTrips = []

st.title('trip finder')

col1, col2 = st.columns([1, 1])
with col1:
    st.text_input('Source Airport 1', 'AUS', disabled=True)
    st.text_input('Source Airport 2', 'JFK', disabled=True)
    start_date = st.date_input('Possible start date', pd.to_datetime('2024-12-01'), disabled=True)
    end_date = st.date_input('Possible end date', pd.to_datetime('2024-12-08'), disabled=True)
    st.text_input('Duration', '5', disabled=True)
    if st.button('get trips'):
        if len(ss.travelData) == 0:
            sourceDataA = {
                'sourceAirport': 'AUS',
                'trips': []
            }
            for i in range(3):
                tripDetails = getTrip(i, "AUS")
                sourceDataA['trips'].append(
                        {
                            'dates': f"Dec {i+1} - Dec {i+6}",
                            "details": tripDetails
                        }
                    )
            ss.travelData.append(sourceDataA) 

            sourceDataB = {
                'sourceAirport': 'JFK',
                'trips': []
            }
            for i in range(3):
                tripDetails = getTrip(i, "JFK")
                sourceDataB['trips'].append(
                        {
                            'dates': f"Dec {i+1} - Dec {i+6}",
                            "details": tripDetails
                        }
                    )
            ss.travelData.append(sourceDataB)   

with col2:
    dates = ['Dec 1 - Dec 6', 'Dec 2 - Dec 7', 'Dec 3 - Dec 8']
    
    ss.filteredTrips = []
    
    if len(ss.filteredTrips): 
        for i in range(len(dates)):
            sourceA = ss.travelData[0]['trips'][i]['details']
            sourceB = ss.travelData[1]['trips'][i]['details']
            for tripA in sourceA:
                for tripB in sourceB:
                    if tripA['destination'] == tripB['destination']:
                        j = 0
                        for j in range(len(ss.filteredTrips)):
                            totalPrice = 0
                            for trip in ss.filteredTrips[j]['trips']:
                                totalPrice += trip['price']
                            if totalPrice > tripA['price'] + tripB['price']:
                                break
                        ss.filteredTrips.insert(j, 
                        {
                            'dates': dates[i],
                            'destination': tripA['destination'],
                            'trips': [{
                                        'source': ss.travelData[0]['sourceAirport'],
                                        'price': tripA['price']
                                    },
                                    {
                                        'source': ss.travelData[1]['sourceAirport'],
                                        'price': tripB['price']
                                    }]
                        })
             
        for trip in ss.filteredTrips:
            with st.expander(f"Go to {trip['destination']} from {trip['dates']}"):
                for trip_detail in trip['trips']:
                    st.write(f"Flights from {trip_detail['source']} to {trip['destination']} start at ${trip_detail['price']}")
    



