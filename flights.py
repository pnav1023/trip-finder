from serpapi import GoogleSearch
from openai import OpenAI
from dotenv import load_dotenv
import os
from pydantic import BaseModel, Field, ValidationError

class Flight(BaseModel):
    departure_id: str = Field(description="The code representing the airport of departure")
    arrival_id: str = Field(description="The code representing the airport of arrival")
    trip_dates: list[str] = Field(description="The list of dates of departure and return")

def get_flights(departure_id, arrival_id, trip_dates):
    load_dotenv()
    
    outbound_date = trip_dates.split("to")[0]
    return_date = trip_dates.split("to")[1]

    params = {
        "api_key": os.getenv("SERP_API_KEY"),
        "engine": "google_flights",
        "hl": "en",
        "gl": "us",
        "departure_id": departure_id,
        "arrival_id": arrival_id,
        "outbound_date": outbound_date,
        "return_date": return_date,
        "currency": "USD",
        "stops": "2",
        "deep_search": "true"
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    return results

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
            trip_dates: which is a list where each element is a string of a departure date and a return date for each trip.
             
            here is a sample response:
            {
                "departure_id": "BOS",
                "arrival_id": "LAX",
                "trip_dates": ["2024-04-17to2024-04-23", "2024-04-24to2024-05-01"]
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

def main():
    flight_queries = process_chat("Today is April 16th, I want to fly from Boston to Austin in April and I want my trip to be exactly 12 days. I want to return before May 1st. What are my options for travel dates?")
    print(flight_queries)

if __name__ == "__main__":
    main()
