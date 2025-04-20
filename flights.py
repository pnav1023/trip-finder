from serpapi import GoogleSearch
from openai import OpenAI
from dotenv import load_dotenv
import os
from pydantic import BaseModel, Field, ValidationError
import datetime
from calendar import monthrange

global_checked_flights = []



test_data = {
   "search_metadata":{
      "id":"6802d52d19705881f83fc091",
      "status":"Success",
      "json_endpoint":"https://serpapi.com/searches/4a0f81e284ce1623/6802d52d19705881f83fc091.json",
      "created_at":"2025-04-18 22:41:49 UTC",
      "processed_at":"2025-04-18 22:41:49 UTC",
      "google_flights_url":"https://www.google.com/travel/flights?hl=en&gl=us&curr=USD&tfs=CBwQAhogEgoyMDI1LTA1LTAxKABqBwgBEgNCT1NyBwgBEgNBVVMaIBIKMjAyNS0wNS0yOSgAagcIARIDQVVTcgcIARIDQk9TQgEBSAFwAZgBAQ&tfu=EgIIAg",
      "raw_html_file":"https://serpapi.com/searches/4a0f81e284ce1623/6802d52d19705881f83fc091.html",
      "prettify_html_file":"https://serpapi.com/searches/4a0f81e284ce1623/6802d52d19705881f83fc091.prettify",
      "total_time_taken":1.28
   },
   "search_parameters":{
      "engine":"google_flights",
      "hl":"en",
      "gl":"us",
      "departure_id":"BOS",
      "arrival_id":"AUS",
      "outbound_date":"2025-05-01",
      "return_date":"2025-05-29",
      "stops":1,
      "currency":"USD",
      "deep_search": True,
      "sort_by":"2"
   },
   "other_flights":[
      {
         "flights":[
            {
               "departure_airport":{
                  "name":"Boston Logan International Airport",
                  "id":"BOS",
                  "time":"2025-05-01 20:05"
               },
               "arrival_airport":{
                  "name":"Austin-Bergstrom International Airport",
                  "id":"AUS",
                  "time":"2025-05-01 23:40"
               },
               "duration":275,
               "airplane":"Airbus A320",
               "airline":"Delta",
               "airline_logo":"https://www.gstatic.com/flights/airline_logos/70px/DL.png",
               "travel_class":"Economy",
               "flight_number":"DL 1677",
               "legroom":"31 in",
               "extensions":[
                  "Average legroom (31 in)",
                  "Free Wi-Fi",
                  "In-seat power & USB outlets",
                  "Live TV",
                  "Carbon emissions estimate: 232 kg"
               ],
               "often_delayed_by_over_30_min": True
            }
         ],
         "total_duration":275,
         "carbon_emissions":{
            "this_flight":233000,
            "typical_for_this_route":273000,
            "difference_percent":-15
         },
         "price":493,
         "type":"Round trip",
         "airline_logo":"https://www.gstatic.com/flights/airline_logos/70px/DL.png",
         "extensions":[
            "Checked baggage for a fee",
            "Bag and fare conditions depend on the return flight"
         ],
         "departure_token":"WyJDalJJU0UweFJteFFhMHR2VTBsQlJHRndaVkZDUnkwdExTMHRMUzB0TFc5NVlYZ3hORUZCUVVGQlIyZERNVk0wUzFjMFZWRkJFZ1pFVERFMk56Y2FDd2lRZ1FNUUFob0RWVk5FT0J4d2tJRUQiLFtbIkJPUyIsIjIwMjUtMDUtMDEiLCJBVVMiLG51bGwsIkRMIiwiMTY3NyJdXV0="
      },
      {
         "flights":[
            {
               "departure_airport":{
                  "name":"Boston Logan International Airport",
                  "id":"BOS",
                  "time":"2025-05-01 06:30"
               },
               "arrival_airport":{
                  "name":"Austin-Bergstrom International Airport",
                  "id":"AUS",
                  "time":"2025-05-01 10:12"
               },
               "duration":282,
               "airplane":"Airbus A220-100 Passenger",
               "airline":"Delta",
               "airline_logo":"https://www.gstatic.com/flights/airline_logos/70px/DL.png",
               "travel_class":"Economy",
               "flight_number":"DL 1410",
               "legroom":"31 in",
               "extensions":[
                  "Average legroom (31 in)",
                  "Free Wi-Fi",
                  "In-seat power & USB outlets",
                  "Live TV",
                  "Carbon emissions estimate: 287 kg"
               ]
            }
         ],
         "total_duration":282,
         "carbon_emissions":{
            "this_flight":288000,
            "typical_for_this_route":273000,
            "difference_percent":5
         },
         "price":658,
         "type":"Round trip",
         "airline_logo":"https://www.gstatic.com/flights/airline_logos/70px/DL.png",
         "extensions":[
            "Checked baggage for a fee",
            "Bag and fare conditions depend on the return flight"
         ],
         "departure_token":"WyJDalJJU0UweFJteFFhMHR2VTBsQlJHRndaVkZDUnkwdExTMHRMUzB0TFc5NVlYZ3hORUZCUVVGQlIyZERNVk0wUzFjMFZWRkJFZ1pFVERFME1UQWFDd2lFZ2dRUUFob0RWVk5FT0J4d2hJSUUiLFtbIkJPUyIsIjIwMjUtMDUtMDEiLCJBVVMiLG51bGwsIkRMIiwiMTQxMCJdXV0="
      },
      {
         "flights":[
            {
               "departure_airport":{
                  "name":"Boston Logan International Airport",
                  "id":"BOS",
                  "time":"2025-05-01 14:15"
               },
               "arrival_airport":{
                  "name":"Austin-Bergstrom International Airport",
                  "id":"AUS",
                  "time":"2025-05-01 17:54"
               },
               "duration":279,
               "airplane":"Airbus A220-100 Passenger",
               "airline":"Delta",
               "airline_logo":"https://www.gstatic.com/flights/airline_logos/70px/DL.png",
               "travel_class":"Economy",
               "flight_number":"DL 1297",
               "legroom":"31 in",
               "extensions":[
                  "Average legroom (31 in)",
                  "Free Wi-Fi",
                  "In-seat power & USB outlets",
                  "Live TV",
                  "Carbon emissions estimate: 287 kg"
               ]
            }
         ],
         "total_duration":279,
         "carbon_emissions":{
            "this_flight":288000,
            "typical_for_this_route":273000,
            "difference_percent":5
         },
         "price":759,
         "type":"Round trip",
         "airline_logo":"https://www.gstatic.com/flights/airline_logos/70px/DL.png",
         "extensions":[
            "Checked baggage for a fee",
            "Bag and fare conditions depend on the return flight"
         ],
         "departure_token":"WyJDalJJU0UweFJteFFhMHR2VTBsQlJHRndaVkZDUnkwdExTMHRMUzB0TFc5NVlYZ3hORUZCUVVGQlIyZERNVk0wUzFjMFZWRkJFZ1pFVERFeU9UY2FDd2o1MEFRUUFob0RWVk5FT0J4dytkQUUiLFtbIkJPUyIsIjIwMjUtMDUtMDEiLCJBVVMiLG51bGwsIkRMIiwiMTI5NyJdXV0="
      },
      {
         "flights":[
            {
               "departure_airport":{
                  "name":"Boston Logan International Airport",
                  "id":"BOS",
                  "time":"2025-05-01 11:05"
               },
               "arrival_airport":{
                  "name":"Austin-Bergstrom International Airport",
                  "id":"AUS",
                  "time":"2025-05-01 14:41"
               },
               "duration":276,
               "airplane":"Airbus A220-300 Passenger",
               "airline":"JetBlue",
               "airline_logo":"https://www.gstatic.com/flights/airline_logos/70px/B6.png",
               "travel_class":"Economy",
               "flight_number":"B6 1039",
               "legroom":"32 in",
               "extensions":[
                  "Above average legroom (32 in)",
                  "Free Wi-Fi",
                  "In-seat power & USB outlets",
                  "Live TV",
                  "Carbon emissions estimate: 261 kg"
               ]
            }
         ],
         "total_duration":276,
         "carbon_emissions":{
            "this_flight":261000,
            "typical_for_this_route":273000,
            "difference_percent":-4
         },
         "price":864,
         "type":"Round trip",
         "airline_logo":"https://www.gstatic.com/flights/airline_logos/70px/B6.png",
         "extensions":[
            "Checked baggage for a fee",
            "Bag and fare conditions depend on the return flight"
         ],
         "departure_token":"WyJDalJJU0UweFJteFFhMHR2VTBsQlJHRndaVkZDUnkwdExTMHRMUzB0TFc5NVlYZ3hORUZCUVVGQlIyZERNVk0wUzFjMFZWRkJFZ1pDTmpFd016a2FDd2o4b2dVUUFob0RWVk5FT0J4dy9LSUYiLFtbIkJPUyIsIjIwMjUtMDUtMDEiLCJBVVMiLG51bGwsIkI2IiwiMTAzOSJdXV0="
      }
   ],
   "price_insights":{
      "lowest_price":493,
      "price_level":"typical",
      "typical_price_range":[
         285,
         495
      ],
      "price_history":[
         [
            1739768400,
            478
         ],
         [
            1739854800,
            433
         ],
         [
            1739941200,
            433
         ],
         [
            1740027600,
            448
         ],
         [
            1740114000,
            448
         ],
         [
            1740200400,
            448
         ],
         [
            1740286800,
            448
         ],
         [
            1740373200,
            448
         ],
         [
            1740459600,
            478
         ],
         [
            1740546000,
            448
         ],
         [
            1740632400,
            448
         ],
         [
            1740718800,
            448
         ],
         [
            1740805200,
            488
         ],
         [
            1740891600,
            408
         ],
         [
            1740978000,
            408
         ],
         [
            1741064400,
            408
         ],
         [
            1741150800,
            408
         ],
         [
            1741237200,
            408
         ],
         [
            1741323600,
            408
         ],
         [
            1741410000,
            408
         ],
         [
            1741496400,
            378
         ],
         [
            1741579200,
            457
         ],
         [
            1741665600,
            457
         ],
         [
            1741752000,
            457
         ],
         [
            1741838400,
            457
         ],
         [
            1741924800,
            457
         ],
         [
            1742011200,
            469
         ],
         [
            1742097600,
            469
         ],
         [
            1742184000,
            428
         ],
         [
            1742270400,
            428
         ],
         [
            1742356800,
            428
         ],
         [
            1742443200,
            477
         ],
         [
            1742529600,
            477
         ],
         [
            1742616000,
            477
         ],
         [
            1742702400,
            477
         ],
         [
            1742788800,
            428
         ],
         [
            1742875200,
            409
         ],
         [
            1742961600,
            409
         ],
         [
            1743048000,
            458
         ],
         [
            1743134400,
            458
         ],
         [
            1743220800,
            458
         ],
         [
            1743307200,
            458
         ],
         [
            1743393600,
            478
         ],
         [
            1743480000,
            409
         ],
         [
            1743566400,
            409
         ],
         [
            1743652800,
            458
         ],
         [
            1743739200,
            458
         ],
         [
            1743825600,
            458
         ],
         [
            1743912000,
            458
         ],
         [
            1743998400,
            487
         ],
         [
            1744084800,
            487
         ],
         [
            1744171200,
            487
         ],
         [
            1744257600,
            457
         ],
         [
            1744344000,
            389
         ],
         [
            1744430400,
            389
         ],
         [
            1744516800,
            389
         ],
         [
            1744603200,
            418
         ],
         [
            1744689600,
            418
         ],
         [
            1744776000,
            458
         ],
         [
            1744862400,
            463
         ],
         [
            1744948800,
            493
         ]
      ]
   },
   "airports":[
      {
         "departure":[
            {
               "airport":{
                  "id":"BOS",
                  "name":"Boston Logan International Airport"
               },
               "city":"Boston",
               "country":"United States",
               "country_code":"US",
               "image":"https://encrypted-tbn0.gstatic.com/licensed-image?q=tbn:ANd9GcQQ-3Qh0_zy2SpQQ2ytZgJKZKCskrzlVnoVoEA2aPGqAnxLN1qkiCfGinwF3UtW6pB3Cx5kAhsFkDWpO-_jICMpLZMQTiEp9APcvTb4s4c",
               "thumbnail":"https://encrypted-tbn0.gstatic.com/licensed-image?q=tbn:ANd9GcRwsXVjxe1Aa5xfa1emRs9kYZl4N9e17ARLpKeInzWjFhyqpXG7oRQxHT-F3RvKcB3W5wf0ini0IdTVcS6lKkdCdJSlC066C8l9HGy4JzM"
            }
         ],
         "arrival":[
            {
               "airport":{
                  "id":"AUS",
                  "name":"Austin-Bergstrom International Airport"
               },
               "city":"Austin",
               "country":"United States",
               "country_code":"US",
               "image":"https://encrypted-tbn3.gstatic.com/images?q=tbn:ANd9GcRKdjkMcBZuGRD1MjnuLQvdGtpTk0RyjdYs0Z8JsPtfIjer-6VvmfmMLxzvBkeyUrhf_focikfda4rVHg",
               "thumbnail":"https://encrypted-tbn3.gstatic.com/images?q=tbn:ANd9GcSQ73FSj9E8pKaNvjWKyEDQGfLV-pky_onARvOY-zHWvQ-hOuPJSqyyXzvyg4-kGGAcZxdO6T5SYGWBzrX8x6MSPq7gBHsSLzX9MYjFJWA"
            }
         ]
      },
      {
         "departure":[
            {
               "airport":{
                  "id":"AUS",
                  "name":"Austin-Bergstrom International Airport"
               },
               "city":"Austin",
               "country":"United States",
               "country_code":"US",
               "image":"https://encrypted-tbn3.gstatic.com/images?q=tbn:ANd9GcRKdjkMcBZuGRD1MjnuLQvdGtpTk0RyjdYs0Z8JsPtfIjer-6VvmfmMLxzvBkeyUrhf_focikfda4rVHg",
               "thumbnail":"https://encrypted-tbn3.gstatic.com/images?q=tbn:ANd9GcSQ73FSj9E8pKaNvjWKyEDQGfLV-pky_onARvOY-zHWvQ-hOuPJSqyyXzvyg4-kGGAcZxdO6T5SYGWBzrX8x6MSPq7gBHsSLzX9MYjFJWA"
            }
         ],
         "arrival":[
            {
               "airport":{
                  "id":"BOS",
                  "name":"Boston Logan International Airport"
               },
               "city":"Boston",
               "country":"United States",
               "country_code":"US",
               "image":"https://encrypted-tbn0.gstatic.com/licensed-image?q=tbn:ANd9GcQQ-3Qh0_zy2SpQQ2ytZgJKZKCskrzlVnoVoEA2aPGqAnxLN1qkiCfGinwF3UtW6pB3Cx5kAhsFkDWpO-_jICMpLZMQTiEp9APcvTb4s4c",
               "thumbnail":"https://encrypted-tbn0.gstatic.com/licensed-image?q=tbn:ANd9GcRwsXVjxe1Aa5xfa1emRs9kYZl4N9e17ARLpKeInzWjFhyqpXG7oRQxHT-F3RvKcB3W5wf0ini0IdTVcS6lKkdCdJSlC066C8l9HGy4JzM"
            }
         ]
      }
   ]
}

class Flight(BaseModel):
    departure_id: str = Field(description="The code representing the airport of departure")
    arrival_id: str = Field(description="The code representing the airport of arrival")
    months: list[str] = Field(description="A list of the months available for travel")
    average_trip_length: float = Field(description="The average number of days the trip will be")
    
    
def get_flights(departure_id, arrival_id, outbound_date):
    load_dotenv()

    if outbound_date in global_checked_flights:
        print(f"{outbound_date} - Recent flight search. Pulling from DB (not implemented)")
      #   return None
    else:
        print(f"{outbound_date} - New flight search. Adding to DB (not implemented)")
        global_checked_flights.append(outbound_date)
      #   return None

    params = {
        "api_key": os.getenv("SERP_API_KEY"),
        "engine": "google_flights",
        "hl": "en",
        "gl": "us",
        "departure_id": departure_id,
        "arrival_id": arrival_id,
        "outbound_date": outbound_date,
        "currency": "USD",
        "stops": "1",
        "deep_search": "true",
        "sort_by": "2",
        "type": "2" # 2 for one way, 1 for round trip
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    return results

def generate_trip_dates(months, trip_length, year):
    """
    Generate all possible trip periods within the specified months of a year.
    
    Args:
        months: List of month names (e.g., ["May", "June"])
        trip_length: Length of the trip in days
        year: The year as an integer
        
    Returns:
        A list of tuples, each containing (start_date, end_date) in "YYYY-MM-DD" format
    """
    # Dictionary to convert month names to their numerical value
    month_to_num = {
        "January": 1, "February": 2, "March": 3, "April": 4,
        "May": 5, "June": 6, "July": 7, "August": 8,
        "September": 9, "October": 10, "November": 11, "December": 12
    }
    
    trip_periods = []
    
    for month_name in months:
        if month_name not in month_to_num:
            continue
            
        month_num = month_to_num[month_name]
        # Get the number of days in the month
        _, days_in_month = monthrange(year, month_num)
        
        # Generate all possible start dates in this month
        for day in range(1, days_in_month + 1):
            start_date = datetime.date(year, month_num, day)
            # Calculate the end date by adding trip_length days
            end_date = start_date + datetime.timedelta(days=trip_length-1) # -1 because the trip length is inclusive of the start and end dates
            
            # Check if the end date is within the allowed range
            if end_date.month == start_date.month:
            # Format dates as YYYY-MM-DD strings
                start_str = start_date.strftime("%Y-%m-%d")
                end_str = end_date.strftime("%Y-%m-%d")
                
                trip_periods.append((start_str, end_str))
    
    return trip_periods

def process_chat(message):
    load_dotenv()

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": message},
            {"role": "system", "content": """You are a helpful assistant that returns a JSON object based on what the user inputted. The JSON object should have the following fields: 
            departure_id: which is the code representing the airport of departure
            arrival_id: which is the code representing the airport of arrival
            months: which is a list where each element is a string of a month available for travel.
            average_trip_length: which is the average number of days the trip will be.
            
            here is a sample response:
            {
                "departure_id": "BOS",
                "arrival_id": "LAX",
                "months": ["May", "June"],
                "average_trip_length": 28,
            }
            """}
        ],
        response_format={"type": "json_object"}
    )

    flight_queries = None
    try:
        flight_queries = Flight.model_validate_json(response.choices[0].message.content)
    except ValidationError as e:
        print(e)

    return flight_queries

def find_cheapest_flights(trip_dates, departure_id, arrival_id):
    cheapest_flight_date = None
    cheapest_flight_departure_url = ""
    cheapest_flight_arrival_url = ""
    cheapest_flight_total_price = 999999999

    for trip_date in trip_dates:
        departure_flight = get_flights(departure_id, arrival_id, trip_date[0])
        arrival_flight = get_flights(arrival_id, departure_id, trip_date[1])

        if departure_flight is None or arrival_flight is None:
            continue

        departure_url = departure_flight["search_metadata"]["google_flights_url"]
        departure_price = departure_flight["price_insights"]["lowest_price"]

        arrival_url = arrival_flight["search_metadata"]["google_flights_url"]
        arrival_price = arrival_flight["price_insights"]["lowest_price"]

        print(f"Trip Date: {trip_date}")
        print(f"Departure URL: {departure_url}")
        print(f"Arrival URL: {arrival_url}")
        print(f"Total Price: {departure_price + arrival_price}")

        if departure_price + arrival_price < cheapest_flight_total_price:
            cheapest_flight_date = trip_date
            cheapest_flight_departure_url = departure_url
            cheapest_flight_arrival_url = arrival_url
            cheapest_flight_total_price = departure_price + arrival_price

    return cheapest_flight_date, cheapest_flight_departure_url, cheapest_flight_arrival_url, cheapest_flight_total_price

def main():
   #  flights = get_flights("BOS", "AUS", "2025-05-01")
   #  print(flights)

    prompt = """I want to fly from Boston to Austin in August 2025 and I want my trip to be exactly 29 days. Find me all the possible travel date options."""

    print(f"Prompt: {prompt}\n")
    flight_queries = process_chat(prompt)
    print(f"Flight Queries: {flight_queries}\n")
    trip_dates = generate_trip_dates(flight_queries.months, flight_queries.average_trip_length, 2025)
    print(f"Trip Dates: {trip_dates}\n")
    cheapest_flight_date, cheapest_flight_departure_url, cheapest_flight_arrival_url, cheapest_flight_total_price = find_cheapest_flights(trip_dates, flight_queries.departure_id, flight_queries.arrival_id)
    print(f"\nCheapest Flight Date: {cheapest_flight_date}")
    print(f"Cheapest Flight Departure URL: {cheapest_flight_departure_url}")
    print(f"Cheapest Flight Arrival URL: {cheapest_flight_arrival_url}")
    print(f"Cheapest Flight Total Price: {cheapest_flight_total_price}")

if __name__ == "__main__":
    main()
