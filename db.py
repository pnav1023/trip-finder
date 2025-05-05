import os
import uuid
from datetime import datetime
from dotenv import load_dotenv
from supabase import create_client
from typing import Optional, List, Dict, Any, Union

SUPABASE_FLIGHT_TABLE="flight_data"

def get_supabase_client():
    load_dotenv(override=True)

    # Supabase connection
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_API_KEY")
    SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)

    return supabase

# CRUD Operations
def create_flight_data(
    supabase,
    flight_date: str,
    flight_url: str,
    flight_price: float,
    departing_airport_code: str,
    arriving_airport_code: str,
    serp_google_result: Optional[Dict] = None  # New JSON field
) -> Dict[str, Any]:
    """
    Create a new flight data record

    Args:
        supabase: The Supabase client instance.
        flight_date: The date of the flight as a string (YYYY-MM-DD).
        flight_url: The URL to the flight details.
        flight_price: The price of the flight.
        departing_airport_code: The departure airport code (e.g., 'BOS').
        arriving_airport_code: The arrival airport code (e.g., 'AUS').
        serp_google_result: JSON result data from SERP API (optional).

    Returns:
        The created flight data object as a dictionary, or None if creation failed.
    """
    data = {
        "flight_date": flight_date,
        "flight_url": flight_url,
        "flight_price": flight_price,
        "departing_airport_code": departing_airport_code,
        "arriving_airport_code": arriving_airport_code,
    }
    
    # Add the serp_google_result if provided
    if serp_google_result is not None:
        data["serp_google_result"] = serp_google_result

    try:
        result = supabase.table(SUPABASE_FLIGHT_TABLE).insert(data).execute()
        # Return the created record
        if result.data:
            return result.data[0]
        else:
            print(f"Error creating flight data: {result.error}")
            return None
    except Exception as e:
        print(f"Exception during flight data creation: {e}")
        return None

def get_flight_data(supabase, flight_id: str) -> Dict[str, Any]:
    """
    Get flight data by ID
    
    Args:
        flight_id: The UUID of the flight data to retrieve
        
    Returns:
        The flight data object if found, None otherwise
    """
    result = supabase.table(SUPABASE_FLIGHT_TABLE).select("*").eq("id", flight_id).execute()
    
    if result.data and len(result.data) > 0:
        return result.data[0]
    return None

def get_all_flight_data(supabase) -> List[Dict[str, Any]]:
    """
    Get all flight data records
    
    Returns:
        List of all flight data objects
    """
    result = supabase.table(SUPABASE_FLIGHT_TABLE).select("*").execute()
    return result.data

def get_flights_by_date(supabase, flight_date: str, departure_id: str, arrival_id: str) -> List[Dict[str, Any]]:
    """
    Get flight data by date and airport

    Args:
        supabase: The Supabase client instance.
        flight_date: The date to filter flights by as a string (YYYY-MM-DD).
        departure_id: The departure airport code (e.g., 'BOS').
        arrival_id: The arrival airport code (e.g., 'AUS').

    Returns:
        List of flight data objects for the specified date
    """
    # Input is already the string format needed for matching
    date_str = flight_date # No longer needs isoformat or strftime

    # Using eq for exact date match
    result = supabase.table(SUPABASE_FLIGHT_TABLE).select("*").eq("flight_date", date_str).eq("departing_airport_code", departure_id).eq("arriving_airport_code", arrival_id).execute()
    return result.data

def update_flight_data(
    supabase,
    flight_id: str,
    flight_date: Optional[str] = None,
    flight_url: Optional[str] = None,
    flight_price: Optional[float] = None,
    departing_airport_code: Optional[str] = None,
    arriving_airport_code: Optional[str] = None,
    serp_google_result: Optional[Dict] = None  # New JSON field
) -> Dict[str, Any]:
    """
    Update flight data by ID

    Args:
        supabase: The Supabase client instance.
        flight_id: The UUID of the flight data to update.
        flight_date: The new date of the flight as a string (YYYY-MM-DD) (optional).
        flight_url: The new URL to the flight details (optional).
        flight_price: The new price of the flight (optional).
        departing_airport_code: The new departure airport code (optional).
        arriving_airport_code: The new arrival airport code (optional).
        serp_google_result: Updated JSON result data from SERP API (optional).

    Returns:
        The updated flight data object if found and updated, None otherwise.
    """
    # Build update data object with only provided fields
    update_data = {}

    if flight_date is not None:
        update_data["flight_date"] = flight_date

    if flight_url is not None:
        update_data["flight_url"] = flight_url

    if flight_price is not None:
        update_data["flight_price"] = flight_price

    if departing_airport_code is not None:
        update_data["departing_airport_code"] = departing_airport_code

    if arriving_airport_code is not None:
        update_data["arriving_airport_code"] = arriving_airport_code
        
    if serp_google_result is not None:
        update_data["serp_google_result"] = serp_google_result

    if not update_data:  # If no updates provided, return current data
        return get_flight_data(supabase, flight_id)

    # Perform update
    try:
        result = supabase.table(SUPABASE_FLIGHT_TABLE) \
            .update(update_data) \
            .eq("id", flight_id) \
            .execute()

        if result.data:
            return result.data[0]
        else:
            # Check if the record exists before concluding an error
            existing_record = get_flight_data(supabase, flight_id)
            if existing_record:
                 print(f"Error updating flight data (ID: {flight_id}): {result.error}")
            else:
                 print(f"Flight data with ID {flight_id} not found for update.")
            return None
    except Exception as e:
        print(f"Exception during flight data update (ID: {flight_id}): {e}")
        return None

def delete_flight_data(supabase, flight_id: str) -> bool:
    """
    Delete flight data by ID
    
    Args:
        flight_id: The UUID of the flight data to delete
        
    Returns:
        True if deleted, False if not found
    """
    result = supabase.table(SUPABASE_FLIGHT_TABLE) \
        .delete() \
        .eq("id", flight_id) \
        .execute()
    
    return result.data is not None and len(result.data) > 0

def delete_all_flight_data(supabase) -> int:
    """
    Delete all flight data records
    
    Returns:
        Number of records deleted
    """
    # First count all records
    count_result = supabase.table(SUPABASE_FLIGHT_TABLE).select("id").execute()
    count = len(count_result.data) if count_result.data else 0
    
    # Then delete all records
    supabase.table(SUPABASE_FLIGHT_TABLE).delete().neq("id", "impossible-value").execute()
    
    return count

def check_flight_exists(supabase, flight_date: str, departure_id: str, arrival_id: str) -> Optional[str]:
    """
    Check if a flight with the given date and URL already exists.

    Args:
        supabase: The Supabase client instance.
        flight_date: The date of the flight as a string (YYYY-MM-DD).
        departure_id: The departure airport code (e.g., 'BOS').
        arrival_id: The arrival airport code (e.g., 'AUS').

    Returns:
        The flight's id (str) if it exists, None otherwise.
    """
    date_str = flight_date

    try:
        result = supabase.table(SUPABASE_FLIGHT_TABLE) \
            .select("id") \
            .eq("flight_date", date_str) \
            .eq("departing_airport_code", departure_id) \
            .eq("arriving_airport_code", arrival_id) \
            .limit(1) \
            .execute()

        if result.data and len(result.data) > 0:
            return result.data[0]['id']
        else:
            return None
    except Exception as e:
        print(f"Exception during check_flight_exists: {e}")
        return None

def main():
    # Dates are now strings in YYYY-MM-DD format
    flights = [
        ["BOS", "AUS", "2025-06-03", 100.0, "https://www.google.com/travel/flights?hl=en&gl=us&curr=USD&tfs=CBwQAhogEgoyMDI1LTA2LTMxKABqBwgBEgNBVVNyBwgBEgNCT1NCAQFIAXABmAEC&tfu=EgIIAg"],
        ["AUS", "BOS", "2025-06-30", 400.0, "https://www.google.com/travel/flights?hl=en&gl=us&curr=USD&tfs=CBwQAhogEgoyMDI1LTA2LTMxKABqBwgBEgNBVVNyBwgBEgNCT1NCAQFIAXABmAEC&tfu=EgIIAg"],
        ["BOS", "AUS", "2025-06-02", 300.0, "https://www.google.com/travel/flights?hl=en&gl=us&curr=USD&tfs=CBwQAhogEgoyMDI1LTA2LTMxKABqBwgBEgNBVVNyBwgBEgNCT1NCAQFIAXABmAEC&tfu=EgIIAg"],
        ["AUS", "BOS", "2025-06-29", 200.0, "https://www.google.com/travel/flights?hl=en&gl=us&curr=USD&tfs=CBwQAhogEgoyMDI1LTA2LTMxKABqBwgBEgNBVVNyBwgBEgNCT1NCAQFIAXABmAEC&tfu=EgIIAg"],
        ["BOS", "AUS", "2025-06-01", 100.0, "https://www.google.com/travel/flights?hl=en&gl=us&curr=USD&tfs=CBwQAhogEgoyMDI1LTA2LTMxKABqBwgBEgNBVVNyBwgBEgNCT1NCAQFIAXABmAEC&tfu=EgIIAg"],
        ["AUS", "BOS", "2025-06-28", 158.0, "https://www.google.com/travel/flights?hl=en&gl=us&curr=USD&tfs=CBwQAhogEgoyMDI1LTA2LTMxKABqBwgBEgNBVVNyBwgBEgNCT1NCAQFIAXABmAEC&tfu=EgIIAg"]
    ]
    print("Starting flight data operations...")
    supabase = get_supabase_client()
    # Example: Create a new flight data record
    for flight in flights:
        new_flight = create_flight_data(
            supabase,
            flight_date=flight[2], # Pass the string directly
            flight_url=flight[4],
            flight_price=flight[3],
            departing_airport_code=flight[0],
            arriving_airport_code=flight[1]
        )
        print(f"Created flight: {new_flight}")

if __name__ == "__main__":
    main()

