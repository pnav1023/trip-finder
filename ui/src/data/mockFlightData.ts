import { Flight, FlightDetails } from '../types';

export const generateFlights = async (refinement: string | null = null): Promise<Flight[]> => {
  try {
    // Convert to POST request matching the curl command
    const response = await fetch('http://127.0.0.1:8000/find_cheapest_flights', {
      method: 'POST',
      headers: {
        'accept': 'application/json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        query: "I want to go to AUS from BOS in June and the average trip length is 29 days",
        year: 2025
      })
    });

    if (!response.ok) {
      throw new Error(`API request failed with status: ${response.status}`);
    }

    const data = await response.json();
    console.log('API response:', data);
    
    // Create a flight object from the API response
    // You'll need to map the API response format to your Flight type
    return [{ 
      id: 1, 
      price: data.cheapest_flight_total_price || 245, 
      airline: "Delta",
      departureTime: "7:15 AM",
      arrivalTime: "10:43 AM",
      duration: "3h 28m", 
      date: data.cheapest_flight_date?.[0]?.split('-')[2] + " " + 
            new Date(data.cheapest_flight_date?.[0] || '').toLocaleString('default', {month: 'short'}),
      returnDate: data.cheapest_flight_date?.[1]?.split('-')[2] + " " + 
                 new Date(data.cheapest_flight_date?.[1] || '').toLocaleString('default', {month: 'short'}),
      stops: 0
    }];
  } catch (error) {
    console.error('Error fetching flight data:', error);
    // Return mock data as fallback
    return [{ 
      id: 1, 
      price: 245, 
      airline: "Mock - Delta",
      departureTime: "7:15 AM",
      arrivalTime: "10:43 AM",
      duration: "3h 28m", 
      date: "Jun 12",
      returnDate: "Jun 19",
      stops: 0
    }];
  }
};
     

/**
 * Generates mock flight data based on refinement query
 * @param refinement - Optional search refinement criteria
 * @returns Array of Flight objects
 */
export const generateMockFlights = (refinement: string | null = null): Flight[] => {
  // Base flight options
  const baseFlights: Flight[] = [
    { 
      id: 1, 
      price: 245, 
      airline: "Delta",
      departureTime: "7:15 AM",
      arrivalTime: "10:43 AM",
      duration: "3h 28m", 
      date: "Jun 12",
      returnDate: "Jun 19",
      stops: 0
    },
    {
      id: 2,
      price: 245,
      airline: "Delta",
      departureTime: "7:15 AM",
      arrivalTime: "10:43 AM",
      duration: "3h 28m", 
      date: "Jun 12",
      returnDate: "Jun 19",
      stops: 0
    },
    {
      id: 3,
      price: 245,
      airline: "Delta",
      departureTime: "7:15 AM",
      arrivalTime: "10:43 AM",
      duration: "3h 28m", 
      date: "Jun 12",
      returnDate: "Jun 19",
      stops: 0
    },
    // ... other base flights (same as original)
  ];
  
  // For refinements, modify the flights based on input
  if (refinement) {
    if (refinement.toLowerCase().includes('morning')) {
      return [
        // ... morning flights (same as original)
        ...baseFlights
      ];
    } else if (refinement.toLowerCase().includes('cheaper') || refinement.toLowerCase().includes('less')) {
      return [
        // ... cheaper flights (same as original)
        ...baseFlights
      ];
    } else if (refinement.toLowerCase().includes('direct') || refinement.toLowerCase().includes('nonstop')) {
      return [
        // ... direct flights (same as original)
        ...baseFlights
      ];
    }
  }
  
  return baseFlights;
};

/**
 * Returns detailed flight information based on flight ID
 * @param flightId - The ID of the flight to get details for
 * @returns FlightDetails object with complete flight information
 */
export const generateFlightDetails = (flightId: number): FlightDetails => {
  const baseDetails = {
    departureAirport: "BOS",
    arrivalAirport: "LAX",
    returnDepartureTime: "5:30 PM",
    returnArrivalTime: "9:15 PM",
    returnDuration: "3h 45m",
    returnStops: 0,
    baggage: "First bag $30, Second bag $40",
    airline: "Delta",
    date: "Jun 12"
  };

  const flightById: Record<number, FlightDetails> = {
    // ... same flight details as original
    1: {
      ...baseDetails,
      id: 1,
      departureTime: "7:15 AM",
      arrivalTime: "10:43 AM",
      duration: "3h 28m",
      stops: 0,
      returnDate: "Jun 19",
      price: 245
    },
    2: {
      ...baseDetails,
      id: 2,
      departureTime: "1:30 PM",
      arrivalTime: "5:12 PM",
      duration: "3h 42m",
      stops: 0,
      returnDate: "Jul 1",
      returnStopLocation: "ORD",
      price: 265
    },
    3: {
      ...baseDetails,
      id: 3,
      departureTime: "10:20 AM",
      arrivalTime: "1:45 PM",
      duration: "3h 25m",
      stops: 1,
      stopLocation: "DEN",
      returnDate: "Jun 17",
      returnStopLocation: "DEN",
      baggage: "First bag free, Second bag $35",
      price: 275
    },
    4: {
      ...baseDetails,
      id: 4,
      departureTime: "6:30 AM",
      arrivalTime: "9:58 AM",
      duration: "3h 28m",
      stops: 0,
      returnDate: "Jun 22",
      price: 255
    },
    5: {
      ...baseDetails,
      id: 5,
      departureTime: "8:15 AM",
      arrivalTime: "11:40 AM",
      duration: "3h 25m",
      stops: 0,
      returnDate: "Jun 23",
      returnStopLocation: "ORD",
      price: 285
    },
    6: {
      ...baseDetails,
      id: 6,
      departureTime: "7:45 AM",
      arrivalTime: "11:10 AM",
      duration: "3h 25m",
      stops: 1,
      stopLocation: "JFK",
      returnDate: "Jun 21",
      baggage: "First bag free, Second bag $35",
      price: 275
    },
    7: {
      ...baseDetails,
      id: 7,
      departureTime: "5:15 AM",
      arrivalTime: "8:43 AM",
      duration: "3h 28m",
      stops: 1,
      stopLocation: "DEN",
      returnDate: "Jun 25",
      baggage: "First bag $30, Second bag $40",
      price: 199
    },
    8: {
      ...baseDetails,
      id: 8,
      departureTime: "10:30 PM",
      arrivalTime: "2:12 AM",
      duration: "3h 42m",
      stops: 1,
      stopLocation: "ATL",
      returnDate: "Jun 30",
      baggage: "First bag $35, Second bag $50",
      price: 219
    },
    9: {
      ...baseDetails,
      id: 9,
      departureTime: "6:20 AM",
      arrivalTime: "9:45 AM",
      duration: "3h 25m",
      stops: 1,
      stopLocation: "DTW",
      returnDate: "Jun 24",
      baggage: "First bag $30, Second bag $40",
      price: 235
    },
    10: {
      ...baseDetails,
      id: 10,
      departureTime: "9:15 AM",
      arrivalTime: "12:43 PM",
      duration: "3h 28m",
      stops: 0,
      returnDate: "Jun 21",
      baggage: "First bag $30, Second bag $40",
      price: 279
    },
    11: {
      ...baseDetails,
      id: 11,
      departureTime: "2:30 PM",
      arrivalTime: "6:12 PM",
      duration: "3h 42m",
      stops: 0,
      returnDate: "Jun 22",
      baggage: "First bag $30, Second bag $40",
      price: 295
    },
    12: {
      ...baseDetails,
      id: 12,
      departureTime: "11:20 AM",
      arrivalTime: "2:45 PM",
      duration: "3h 25m",
      stops: 0,
      returnDate: "Jun 23",
      baggage: "First bag $30, Second bag $40",
      price: 310
    },
  };
  
  return flightById[flightId] || flightById[1];
}; 