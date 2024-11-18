import json 

def formatFlights(data):
    common_destinations_by_dates = {}

    # Process each airport's trips and structure data by dates, destination, and source prices
    for airport_data in data:
        source = airport_data["sourceAirport"]
        for trip in airport_data["trips"]:
            date_range = trip["dates"]
            
            if date_range not in common_destinations_by_dates:
                common_destinations_by_dates[date_range] = {}
            
            for detail in trip["details"]:
                destination = detail["destination"]
                price = detail["price"]
                
                if destination not in common_destinations_by_dates[date_range]:
                    common_destinations_by_dates[date_range][destination] = []
                
                common_destinations_by_dates[date_range][destination].append({
                    "source": source,
                    "price": price
                })

    # Filter out destinations that are not common across all source airports
    final_common_destinations = []

    for date_range, destinations in common_destinations_by_dates.items():
        for destination, trips in destinations.items():
            if len(trips) == len(data):  # Destination must appear in all source airports for this date range
                final_common_destinations.append({
                    "dates": date_range,
                    "destination": destination,
                    "trips": trips,
                    "total_price": sum(trip["price"] for trip in trips)
                })
    # Sort the final common destinations by the sum of the prices of the flights from each source airport
    final_common_destinations.sort(key=lambda x: sum(trip["price"] for trip in x["trips"]))
    # Output the result
    return final_common_destinations
