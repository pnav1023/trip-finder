from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from math import floor, ceil

def formatTripDetails(results):
    formattedTripDetails = []
    for i in range(floor(len(results)/4)):
        formattedTripDetails.append(results[i*4]+"-"+results[i*4+3])
    return formattedTripDetails

def getTrip(days):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.google.com/travel/flights")
    time.sleep(5)

    # tripTypePath = "/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[1]/div[1]/div"
    # tripTypeButton = driver.find_element(By.XPATH, tripTypePath)
    # tripTypeButton.click()

    # oneWayPath = "/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[1]/div[1]/div/div/div/div[2]/ul/li[2]"
    # oneWayButton = driver.find_element(By.XPATH, oneWayPath)
    # oneWayButton.click()

    calendarButtonPath = "/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[2]/div/div/div[1]/div" 
    calendarButton = driver.find_element(By.XPATH, calendarButtonPath)
    calendarButton.click()
    time.sleep(3)

    departureDay = days % 7 + 1
    departureWeek = ceil((days+1)/7)
    departurePath = f"/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div[1]/div/div[2]/div[3]/div[{departureWeek}]/div[{departureDay}]"
    returnDay = (days+5) % 7 + 1
    returnWeek = ceil((departureDay+5)/7)
    returnPath =    f"/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div[1]/div/div[2]/div[3]/div[{returnWeek}]/div[{returnDay}]"
    print("depart"+departurePath)
    departureDateClick = driver.find_element(By.XPATH, departurePath)
    departureDateClick.click()
    time.sleep(1)
    print("return"+returnPath)
    returnDateClick = driver.find_element(By.XPATH, returnPath)
    returnDateClick.click()

    donePath = "/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[2]/div/div/div[2]/div/div[3]/div[3]/div/button"
    doneButton = driver.find_element(By.XPATH, donePath)
    doneButton.click()

    searchButtonPath = "/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[2]/div/button/span[1]"
    searchButtonPath = driver.find_element(By.XPATH, searchButtonPath)
    searchButtonPath.click()
    time.sleep(8)

    resultsPath = "/html/body/c-wiz[3]/div/div[2]/c-wiz/div[2]/div/div/div[1]/main/div/div[2]/div/ol"
    results = driver.find_element(By.XPATH, resultsPath)
    tripDetails = formatTripDetails(results.text.split("\n"))
    driver.quit()

    return tripDetails

if __name__ == "__main__":
    driver = webdriver.Chrome()
    trip_details = getTrip(driver)
    print(trip_details)


