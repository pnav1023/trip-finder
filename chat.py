from pydantic import BaseModel, Field, ValidationError
from openai import OpenAI
from dotenv import load_dotenv
import os
import datetime
from calendar import monthrange

class Flight(BaseModel):
    departure_id: str = Field(..., description="The departure airport code")
    arrival_id: str = Field(..., description="The arrival airport code")
    months: list[str] = Field(..., description="The months of travel")
    average_trip_length: int = Field(..., description="The average trip length")

def generate_api_payloads(departure_airport_ids, arrival_airport_id, months, average_trip_length):
    payloads = []
    trip_periods = generate_trip_dates(months, average_trip_length, 2025)
    for departure_airport_id in departure_airport_ids.split(","):
        for trip_period in trip_periods:
            payloads.append({
                "trip_period": trip_period[0],
                "departure_airport_id": departure_airport_id.strip(),
                "arrival_airport_id": arrival_airport_id.strip(),
            })
            payloads.append({
                "trip_period": trip_period[1],
                "departure_airport_id": arrival_airport_id.strip(),
                "arrival_airport_id": departure_airport_id.strip(),
            })
    return payloads

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
    month_nums = [month_to_num[month_name] for month_name in months if month_name in month_to_num]
    
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
            
            if end_date.month in month_nums:
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

if __name__ == "__main__":
    "I want to go to LAX from BOS in May and June and the average trip length is 28 days"
    load_dotenv()
    # departure_airport_ids = input("Enter the airport codes of the departure airports in a comma separated list: ")
    # arrival_airport_id = input("Enter the airport code of the arrival airport: ")
    # months = input("Enter the months of travel in a comma separated list: ")
    # average_trip_length = input("Enter the average trip length: ")

    departure_airport_ids = "BOS,LAX,AUS,ORH"
    arrival_airport_id = "SFO"
    months = "February"
    average_trip_length = 28

    message = f"I want to go to {arrival_airport_id} from {departure_airport_ids} in {months} and the average trip length is {average_trip_length} days"
    payloads = generate_api_payloads(departure_airport_ids, arrival_airport_id, months.split(","), average_trip_length)
    for i, payload in enumerate(payloads):
        try:
            if i % 2 == 0:
                print(f"{payloads[i]} - {payloads[i+1]}")
                print("-"*100)
        except:
            print("done")
            pass