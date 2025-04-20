import os
import uuid
from datetime import datetime
from dotenv import load_dotenv
from supabase import create_client
from typing import Optional, List, Dict, Any, Union

# Load environment variables
load_dotenv()

# Supabase connection
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_API_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Table name constant
FLIGHT_TABLE = "flight_data"

# CRUD Operations
def create_flight_data(flight_date: datetime, flight_url: str, flight_price: float) -> Dict[str, Any]:
    """
    Create a new flight data record
    
    Args:
        flight_date: The date of the flight
        flight_url: The URL to the flight details
        flight_price: The price of the flight
        
    Returns:
        The created flight data object
    """
    new_id = str(uuid.uuid4())
    
    data = {
        "id": new_id,
        "created_at": datetime.now().isoformat(),
        "flight_date": flight_date.isoformat(),
        "flight_url": flight_url,
        "flight_price": flight_price
    }
    
    result = supabase.table(FLIGHT_TABLE).insert(data).execute()
    
    # Return the created record
    if result.data:
        return result.data[0]
    return None

def get_flight_data(flight_id: str) -> Dict[str, Any]:
    """
    Get flight data by ID
    
    Args:
        flight_id: The UUID of the flight data to retrieve
        
    Returns:
        The flight data object if found, None otherwise
    """
    result = supabase.table(FLIGHT_TABLE).select("*").eq("id", flight_id).execute()
    
    if result.data and len(result.data) > 0:
        return result.data[0]
    return None

def get_all_flight_data() -> List[Dict[str, Any]]:
    """
    Get all flight data records
    
    Returns:
        List of all flight data objects
    """
    result = supabase.table(FLIGHT_TABLE).select("*").execute()
    return result.data

def get_flights_by_date(flight_date: datetime) -> List[Dict[str, Any]]:
    """
    Get flight data by date
    
    Args:
        flight_date: The date to filter flights by
        
    Returns:
        List of flight data objects for the specified date
    """
    # Convert datetime to string format that Supabase expects (ISO format)
    date_str = flight_date.isoformat()
    
    # Using eq for exact date match
    result = supabase.table(FLIGHT_TABLE).select("*").eq("flight_date", date_str).execute()
    return result.data

def get_flights_by_price_range(min_price: float, max_price: float) -> List[Dict[str, Any]]:
    """
    Get flight data within a price range
    
    Args:
        min_price: The minimum price
        max_price: The maximum price
        
    Returns:
        List of flight data objects within the specified price range
    """
    result = supabase.table(FLIGHT_TABLE) \
        .select("*") \
        .gte("flight_price", min_price) \
        .lte("flight_price", max_price) \
        .execute()
    
    return result.data

def get_cheapest_flight() -> Dict[str, Any]:
    """
    Get the cheapest flight
    
    Returns:
        The flight data object with the lowest price
    """
    result = supabase.table(FLIGHT_TABLE) \
        .select("*") \
        .order("flight_price", ascending=True) \
        .limit(1) \
        .execute()
    
    if result.data and len(result.data) > 0:
        return result.data[0]
    return None

def update_flight_data(
    flight_id: str, 
    flight_date: Optional[datetime] = None, 
    flight_url: Optional[str] = None, 
    flight_price: Optional[float] = None
) -> Dict[str, Any]:
    """
    Update flight data by ID
    
    Args:
        flight_id: The UUID of the flight data to update
        flight_date: The new date of the flight (optional)
        flight_url: The new URL to the flight details (optional)
        flight_price: The new price of the flight (optional)
        
    Returns:
        The updated flight data object if found, None otherwise
    """
    # Build update data object with only provided fields
    update_data = {}
    
    if flight_date is not None:
        update_data["flight_date"] = flight_date.isoformat()
    
    if flight_url is not None:
        update_data["flight_url"] = flight_url
    
    if flight_price is not None:
        update_data["flight_price"] = flight_price
    
    if not update_data:  # If no updates provided
        return get_flight_data(flight_id)
    
    # Perform update
    result = supabase.table(FLIGHT_TABLE) \
        .update(update_data) \
        .eq("id", flight_id) \
        .execute()
    
    if result.data and len(result.data) > 0:
        return result.data[0]
    return None

def delete_flight_data(flight_id: str) -> bool:
    """
    Delete flight data by ID
    
    Args:
        flight_id: The UUID of the flight data to delete
        
    Returns:
        True if deleted, False if not found
    """
    result = supabase.table(FLIGHT_TABLE) \
        .delete() \
        .eq("id", flight_id) \
        .execute()
    
    return result.data is not None and len(result.data) > 0

def delete_all_flight_data() -> int:
    """
    Delete all flight data records
    
    Returns:
        Number of records deleted
    """
    # First count all records
    count_result = supabase.table(FLIGHT_TABLE).select("id").execute()
    count = len(count_result.data) if count_result.data else 0
    
    # Then delete all records
    supabase.table(FLIGHT_TABLE).delete().neq("id", "impossible-value").execute()
    
    return count

def check_flight_exists(flight_date: datetime, flight_url: str) -> bool:
    """
    Check if a flight with the given date and URL already exists
    
    Args:
        flight_date: The date of the flight
        flight_url: The URL of the flight
        
    Returns:
        True if exists, False otherwise
    """
    date_str = flight_date.isoformat()
    
    result = supabase.table(FLIGHT_TABLE) \
        .select("id") \
        .eq("flight_date", date_str) \
        .eq("flight_url", flight_url) \
        .execute()
    
    return result.data is not None and len(result.data) > 0
