from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.core.os_manager import ChromeType
import time
from math import floor, ceil
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys


TRIP_LENGTH = 5

def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-gpu")
    options.add_argument("--headless")
    return webdriver.Chrome(
        service=Service(
            ChromeDriverManager().install() #chrome_type=ChromeType.CHROMIUM
        ),
        options=options,
    )

def testScraper():
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-gpu")
    options.add_argument("--headless")

    driver = webdriver.Chrome(
            service=Service(
                ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()
            ),
            options=options,
        )
    driver.get("http://example.com")
    pageSource = driver.page_source
    time.sleep(5)
    driver.quit()

    return pageSource

def formatTripDetails(results):
    results = results.text.split("\n")
    formattedTripDetails = []
    for i in range(floor(len(results)/4)):
        if len(formattedTripDetails) == 10: # added for POC purposes, more string validation needs to be done before removing this
            break
        price = results[i*4+3].replace("$", "")
        if "hr" not in price:
            price = int(price)
        formattedTripDetails.append(
            {
                "destination": results[i*4],
                "price": price
            }
        )
    return formattedTripDetails

def insertLocation(driver, sourceAirport):
    locationPath = "/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[1]/div[1]/div/div/div[1]/div/div/input"
    WebDriverWait(driver, 40).until(
        EC.presence_of_element_located((By.XPATH, locationPath))
    )   
    locationInput = driver.find_element(By.XPATH, locationPath)
    locationInput.clear()
    locationInput.send_keys(sourceAirport)
    firstOptionPath = "/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[1]/div[6]/div[3]/ul/li"
                    
    WebDriverWait(driver, 40).until(
        EC.presence_of_element_located((By.XPATH, firstOptionPath))
    )
    firstOption = driver.find_element(By.XPATH, firstOptionPath)
    firstOption.click()

def insertInputs(driver, days):
    calendarButtonPath = "/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[2]/div/div/div[1]/div" 
    WebDriverWait(driver, 40).until(
        EC.presence_of_element_located((By.XPATH, calendarButtonPath))
    )
    calendarButton = driver.find_element(By.XPATH, calendarButtonPath)
    calendarButton.click()

    departureDay = days % 7 + 1
    departureWeek = ceil((days+1)/7)
    departurePath = f"/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div[1]/div/div[2]/div[3]/div[{departureWeek}]/div[{departureDay}]"
    returnDay = (days+TRIP_LENGTH) % 7 + 1
    returnWeek = ceil((departureDay+TRIP_LENGTH)/7)
    returnPath =    f"/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div[1]/div/div[2]/div[3]/div[{returnWeek}]/div[{returnDay}]"
    print("depart"+departurePath)

    WebDriverWait(driver, 40).until(
        EC.presence_of_element_located((By.XPATH, departurePath))
    )
    departureDateClick = driver.find_element(By.XPATH, departurePath)
    departureDateClick.click()
    
    print("return"+returnPath)
    WebDriverWait(driver, 40).until(
        EC.presence_of_element_located((By.XPATH, returnPath))
    )
    returnDateClick = driver.find_element(By.XPATH, returnPath)
    returnDateClick.click()

    donePath = "/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[2]/div/div/div[2]/div/div[3]/div[3]/div/button"
    WebDriverWait(driver, 40).until(
        EC.presence_of_element_located((By.XPATH, donePath))
    )
    doneButton = driver.find_element(By.XPATH, donePath)
    doneButton.click()

    

def getResults(driver):
    searchButtonPath = "/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[2]/div/button/span[1]"
    WebDriverWait(driver, 40).until(
        EC.presence_of_element_located((By.XPATH, searchButtonPath))
    )
    searchButtonPath = driver.find_element(By.XPATH, searchButtonPath)
    searchButtonPath.click()

    resultsPath = "/html/body/c-wiz[3]/div/div[2]/c-wiz/div[2]/div/div/div[1]/main/div/div[2]/div/ol"
    WebDriverWait(driver, 40).until(
        EC.presence_of_element_located((By.XPATH, resultsPath))
    )
    return driver.find_element(By.XPATH, resultsPath)

def getTrip(days, sourceAirport):
    driver = get_driver()
    driver.get("https://www.google.com/travel/flights")
    insertInputs(driver, days)
    insertLocation(driver, sourceAirport)
    
    rawTripDetails = getResults(driver)

    tripDetails = formatTripDetails(rawTripDetails)
    # driver.quit()

    return tripDetails

if __name__ == "__main__":
    for i in range(3):
        trip_details = getTrip(i, "AUS")
        print(trip_details)
    for i in range(3):
        trip_details = getTrip(i, "JFK")
        print(trip_details)


