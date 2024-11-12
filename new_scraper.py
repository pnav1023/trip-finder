import streamlit as st

"""
## Web scraping on Streamlit Cloud with Selenium

[![Source](https://img.shields.io/badge/View-Source-<COLOR>.svg)](https://github.com/snehankekre/streamlit-selenium-chrome/)

This is a minimal, reproducible example of how to scrape the web with Selenium and Chrome on Streamlit's Community Cloud.

Fork this repo, and edit `/streamlit_app.py` to customize this app to your heart's desire. :heart:
"""

with st.echo():
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager
    from webdriver_manager.core.os_manager import ChromeType
    from selenium.webdriver.support.ui import WebDriverWait 
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.by import By
    from math import floor, ceil
    TRIP_LENGTH = 5

    @st.cache_resource
    def get_driver():
        return webdriver.Chrome(
            service=Service(
                ChromeDriverManager().install() #chrome_type=ChromeType.CHROMIUM
            ),
            options=options,
        )
    
    def insertInputs(driver, days):
        calendarButtonPath = "/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[2]/div/div/div[1]/div" 
        WebDriverWait(driver, 40).until(
            EC.presence_of_element_located((By.XPATH, calendarButtonPath))
        )
        calendarButton = driver.find_element(By.XPATH, calendarButtonPath)
        calendarButton.click()

        # departureDay = days % 7 + 1
        # departureWeek = ceil((days+1)/7)
        # departurePath = f"/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div[1]/div/div[2]/div[3]/div[{departureWeek}]/div[{departureDay}]"
        # returnDay = (days+TRIP_LENGTH) % 7 + 1
        # returnWeek = ceil((departureDay+TRIP_LENGTH)/7)
        # returnPath =    f"/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div[1]/div/div[2]/div[3]/div[{returnWeek}]/div[{returnDay}]"
        # print("depart"+departurePath)

        # WebDriverWait(driver, 40).until(
        #     EC.presence_of_element_located((By.XPATH, departurePath))
        # )
        # departureDateClick = driver.find_element(By.XPATH, departurePath)
        # departureDateClick.click()

        # print("return"+returnPath)
        # WebDriverWait(driver, 40).until(
        #     EC.presence_of_element_located((By.XPATH, returnPath))
        # )
        # returnDateClick = driver.find_element(By.XPATH, returnPath)
        # returnDateClick.click()


    options = Options()
    options.add_argument("--disable-gpu")
    options.add_argument("--headless")

    driver = get_driver()
    driver.get("https://www.google.com/travel/flights")

    insertInputs(driver, 5)

    st.code(driver.page_source)