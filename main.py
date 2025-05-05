from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Tuple, List
import datetime
from fastapi.middleware.cors import CORSMiddleware
# Assuming your existing functions are in flights.py and db.py
# Make sure these imports work based on your project structure
from flights import process_chat, generate_trip_dates, find_cheapest_flights, Flight

# --- Pydantic Models ---

class FlightQueryRequest(BaseModel):
    """Request model for the user's flight query."""
    query: str
    year: int = datetime.datetime.now().year # Default to current year

class CheapestFlightResponse(BaseModel):
    """Response model for the cheapest flight found."""
    cheapest_flight_date: Optional[Tuple[str, str]] = None
    cheapest_flight_departure_url: Optional[str] = None
    cheapest_flight_arrival_url: Optional[str] = None
    cheapest_flight_total_price: Optional[float] = None
    message: Optional[str] = None # For status messages or errors

# --- FastAPI App ---

app = FastAPI(
    title="Flight Search API",
    description="API to find the cheapest flight options based on user queries.",
    version="0.1.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Your frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- API Endpoint ---

@app.post("/find_cheapest_flights", response_model=CheapestFlightResponse)
async def find_cheapest_flights_endpoint(request: FlightQueryRequest):
    """
    Processes a natural language query to find the cheapest flight options.
    """
    print(f"Received query: {request.query} for year {request.year}")

    # 1. Process the chat query to get structured flight parameters
    try:
        flight_queries: Optional[Flight] = process_chat(request.query)
        if not flight_queries:
            raise HTTPException(status_code=400, detail="Could not parse flight query from the input.")
        print(f"Parsed flight queries: {flight_queries}")
    except Exception as e:
        print(f"Error processing chat: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing chat query: {e}")

    # 2. Generate possible trip dates
    try:
        trip_dates: List[Tuple[str, str]] = generate_trip_dates(
            flight_queries.months,
            int(flight_queries.average_trip_length), # Ensure it's an int
            request.year
        )
        if not trip_dates:
            return CheapestFlightResponse(message="No valid trip dates generated for the given criteria.")
        print(f"Generated {len(trip_dates)} possible trip dates.")
    except Exception as e:
        print(f"Error generating trip dates: {e}")
        raise HTTPException(status_code=500, detail=f"Error generating trip dates: {e}")

    # 3. Find the cheapest flights among the generated dates
    try:
        cheapest_date, dep_url, arr_url, total_price = find_cheapest_flights(
            trip_dates,
            flight_queries.departure_id,
            flight_queries.arrival_id
        )
        print(f"Found cheapest flight: Date={cheapest_date}, Price={total_price}")

        if cheapest_date:
            # Save the flight data to the database
            return CheapestFlightResponse(
                cheapest_flight_date=cheapest_date,
                cheapest_flight_departure_url=dep_url,
                cheapest_flight_arrival_url=arr_url,
                cheapest_flight_total_price=total_price,
                message="Cheapest flight found."
            )
        else:
            return CheapestFlightResponse(message="Could not find any flights for the specified dates and criteria.")

    except Exception as e:
        print(f"Error finding cheapest flights: {e}")
        # Consider more specific error handling based on find_cheapest_flights potential issues
        raise HTTPException(status_code=500, detail=f"Error searching for flights: {e}")

# --- Optional: Root endpoint for basic check ---
@app.get("/")
async def read_root():
    return {"message": "Welcome to the Flight Search API"}

# --- To run the app (using uvicorn) ---
# uvicorn main:app --reload