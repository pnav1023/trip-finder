import streamlit as st
from scraper import getTrip, testScraper

st.title('trip finder')

if st.button('get trips'):
    for i in range(9):
        tripDetails = getTrip(i)
        st.write(f"Dec {i+1} - Dec {i+6}")
        st.write(tripDetails)

if st.button('test scraper'):
    st.write('testing scraper 1')
    st.code(testScraper())

