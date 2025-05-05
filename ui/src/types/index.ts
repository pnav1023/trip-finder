/**
 * Types for the flight search application
 */

export interface Flight {
  id: number;
  price: number;
  airline: string;
  departureTime: string;
  arrivalTime: string;
  duration: string;
  date: string;
  returnDate: string;
  stops: number;
}

export interface FlightDetails extends Flight {
  departureAirport: string;
  arrivalAirport: string;
  stopLocation?: string;
  returnDepartureTime: string;
  returnArrivalTime: string;
  returnDuration: string;
  returnStops: number;
  returnStopLocation?: string;
  baggage: string;
}

export interface ChatMessage {
  type: 'user' | 'system';
  text: string;
  flights?: Flight[];
} 