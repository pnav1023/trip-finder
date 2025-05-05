from serpapi.google_search import GoogleSearch
from openai import OpenAI
from dotenv import load_dotenv
import os
from pydantic import BaseModel, Field, ValidationError
import datetime
from calendar import monthrange

from db import check_flight_exists, create_flight_data, get_flight_data, get_supabase_client

global_checked_flights = []

class Flight(BaseModel):
    departure_id: str = Field(description="The code representing the airport of departure")
    arrival_id: str = Field(description="The code representing the airport of arrival")
    months: list[str] = Field(description="A list of the months available for travel")
    average_trip_length: float = Field(description="The average number of days the trip will be")
    
    
def get_flights(departure_id, arrival_id, outbound_date):
   load_dotenv()

   supabase = get_supabase_client()
   flight_id = check_flight_exists(supabase, outbound_date, departure_id, arrival_id)
   if flight_id is not None:
      print(f"{outbound_date} - Recent flight search. Pulling from DB")
      flight_data = get_flight_data(supabase, flight_id)
      return flight_data["serp_google_result"]
   else:
      print(f"{outbound_date} - New flight search. Adding to DB")
      global_checked_flights.append(outbound_date)
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

      # Create flight data with full SERP results
      create_flight_data(
         supabase,
         flight_date=outbound_date,
         flight_url=results["search_metadata"]["google_flights_url"],
         flight_price=results["price_insights"]["lowest_price"],
         departing_airport_code=departure_id,
         arriving_airport_code=arrival_id,
         serp_google_result=results  # Store the complete results JSON
      )

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

      #   print(f"Trip Date: {trip_date}")
      #   print(f"Departure URL: {departure_url}")
      #   print(f"Arrival URL: {arrival_url}")
      #   print(f"Total Price: {departure_price + arrival_price}")

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
