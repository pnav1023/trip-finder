import agentql
from playwright.sync_api import sync_playwright
from time import sleep
from lxml import html
import re
from collections import defaultdict

def order_common_trips_by_total_price(common_destinations, num_sources):
    """
    Orders common trips by total price, considering the same destination,
    start date, end date, and trips from different sources.

    :param common_destinations: List of destinations with grouped trips.
    :return: List of common trips ordered by total price.
    """
    # Group common trips by destination, start date, and end date
    grouped_trips = defaultdict(list)

    for destination_data in common_destinations:
        destination = destination_data["destination"]
        for trip in destination_data["trips"]:
            key = (destination, trip["start_date"], trip["end_date"])
            grouped_trips[key].append(trip)

    # Build result with total price
    trips_with_total_price = []
    for (destination, start_date, end_date), trips in grouped_trips.items():
        if len({trip['source'] for trip in trips}) == num_sources:  # Ensure trips are from different sources
            total_price = sum(int(trip['price'].strip('$')) for trip in trips)
            trips_with_total_price.append({
                "destination": destination,
                "start_date": start_date,
                "end_date": end_date,
                "trips": trips,
                "total_price": total_price
            })

    # Sort trips by total price
    sorted_trips = sorted(trips_with_total_price, key=lambda x: x["total_price"])

    return sorted_trips

def find_common_destinations(data, num_sources):
    """
    Groups trips by destination and returns only those destinations
    that have trips from multiple sources.
    
    :param data: List of trip dictionaries.
    :return: List of destinations with trips grouped by source.
    """
    # Dictionary to store destinations with their sources
    destinations = defaultdict(list)

    # Group trips by destination
    for trip in data:
        destinations[trip['destination']].append(trip)

    # Filter destinations with multiple sources
    common_destinations = [
        {
            "destination": destination,
            "trips": trips
        }
        for destination, trips in destinations.items() if len({trip['source'] for trip in trips}) == num_sources
    ]

    return common_destinations

# Example usage:
# data = [INSERT YOUR DATA HERE]
# common_destinations = find_common_destinations(data)
# print(common_destinations)


def formatFlights(flights, source, start_date, end_date):
    # List to store parsed results
    result = []

    # Regex pattern to match the data
    pattern = r"(?P<location>[A-Za-z\s]+)(?P<number_of_stops>Nonstop|\d+ stop)(?P<duration>(?:\d+ hr)?(?: \d+ min)?)(?P<price>\$\d+)"

    # Parse matches
    for line in flights:
        match = re.match(pattern, line)
        if match:
            result.append({
                "start_date": start_date,
                "end_date": end_date,
                "source": source,
                "destination": match.group("location").strip(),
                "number_of_stops": match.group("number_of_stops"),
                "duration": match.group("duration").strip(),
                "price": match.group("price")
            })

    # Print the result
    return result


def getTrip(source, start_date, end_date):
    # Initialise the browser
    with sync_playwright() as playwright, playwright.chromium.launch(headless=True) as browser:
        page = agentql.wrap(browser.new_page())
        page.goto("https://www.google.com/travel/flights")
        # page.wait_for_page_ready_state()

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
        response.modal.start_location.clear()
        response.modal.start_location.type(source)

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
        response.modal.locations[0].click()

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

        DEPARTURE_DATE = f"""
        {{
            modal {{
                departure_date({start_date} on the calendar)
                return_date({end_date} on the calendar)
                done_button(the button to confirm the dates)
            }}
        }}
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
        source_html = page.content()
        resultsPath = "/html/body/c-wiz[3]/div/div[2]/c-wiz/div[2]/div/div/div[1]/main/div/div[2]/div/ol/li"
        tree = html.fromstring(source_html)
        results = tree.xpath(resultsPath)
        rawFlightData = []
        for result in results:
            rawFlightData.append(result.text_content())
        
        formattedFlights = formatFlights(rawFlightData, source, start_date, end_date)
        print("Processed "+source+" "+start_date+"-"+end_date)
        return formattedFlights

def test():
    dates = [("December 1st 2024", "December 5th 2024"), ("December 2nd 2024", "December 6th 2024"), ("December 3rd 2024", "December 7th 2024")]
    airports = ["JFK", "AUS", "ORD"]
    allTrips = []
    for date in dates:
        for airport in airports:
            trips = getTrip(airport, date[0], date[1])
            allTrips.extend(trips)
    
    commonDestinations = find_common_destinations(allTrips, len(airports))
    orderedCommonDestinations = order_common_trips_by_total_price(commonDestinations, len(airports))
    return orderedCommonDestinations

if __name__ == "__main__":
    dates = [("December 1st 2024", "December 5th 2024"), ("December 2nd 2024", "December 6th 2024"), ("December 3rd 2024", "December 7th 2024")]
    airports = ["JFK", "AUS", "ORD"]
    allTrips = []
    for date in dates:
        for airport in airports:
            trips = getTrip(airport, date[0], date[1])
            allTrips.extend(trips)
    
    commonDestinations = find_common_destinations(allTrips, len(airports))
    orderedCommonDestinations = order_common_trips_by_total_price(commonDestinations, len(airports))
    print(orderedCommonDestinations)
    