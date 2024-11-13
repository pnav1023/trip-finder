import agentql
from playwright.sync_api import sync_playwright
from time import sleep
import json

def getTrip():
    # Initialise the browser
    with sync_playwright() as playwright, playwright.chromium.launch(headless=False) as browser:
        page = agentql.wrap(browser.new_page())
        page.goto("https://www.google.com/travel/flights")

        # Define a query for modal dialog's search input
        STARTING_LOCATION = """
        {
            modal {
                start_location
            }
        }
        """

        # Get the modal's search input and fill it with "Quick Start"
        response = page.query_elements(STARTING_LOCATION)
        # time.sleep(5)
        response.modal.start_location.clear()
        response.modal.start_location.type("JFK")

        # Define a query for the search results
        STARTING_LOCATIONS = """
        {
            modal {
                locations[]
            }
        }
        """

        # Execute the query after the results have returned then click on the first one
        response = page.query_elements(STARTING_LOCATIONS)
        sleep(1)
        response.modal.locations[1].click()

        DEPARTURE = """
        {
            modal {
                departure_input(field to input the departing date for the flight with the calendar icon)
            }
        }
        """

        response = page.query_elements(DEPARTURE)
        response.modal.departure_input.click()
        sleep(1)

        DEPARTURE_DATE = """
        {
            modal {
                departure_date(December 1st 2024 on the calendar)
                return_date(December 5th 2024 on the calendar)
                done_button(the button to confirm the dates)
            }
        }
        """

        response = page.query_elements(DEPARTURE_DATE)
        response.modal.departure_date.click()
        response.modal.return_date.click()
        response.modal.done_button.click()
        sleep(1)

        EXPLORE = """
        {
            modal {
                explore_button(the button to explore the flights with the search icon)
            }
        }
        """

        response = page.query_elements(EXPLORE)
        response.modal.explore_button.click()

        sleep(5)

        TRIPS = """
        {
            modal {
                flight_data[] {
                    flight_location(name of the city)
                    flight_price(price of the flight)
                }
            }
        }
        """

        response = page.query_elements(TRIPS)
        # print(type(response.modal.flight_data))
        # for flight in response.modal.flight_data:
        #     print(flight["flight_location"])#.flight_location["name"], flight.flight_price["name"])
        # sleep(10)

        flights_data = []
        for flight in response.modal.flight_data:
            flight_location_name = flight.flight_location.text_content()
            flight_price_name = flight.flight_price.text_content()
            flights_data.append({
                "flight_location": flight_location_name,
                "flight_price": flight_price_name
            })

        # flights_json = json.dumps(flights_data)
        return flights_data
        # Used only for demo purposes. It allows you to see the effect of the script.
        page.wait_for_timeout(10000)