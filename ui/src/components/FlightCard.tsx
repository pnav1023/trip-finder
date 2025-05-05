import React from 'react';
import { ChevronDown, ChevronUp, Calendar, Clock } from 'lucide-react';
import { Flight } from '../types';
import { AIRLINES } from '../constants/airlines';

interface FlightCardProps {
  flight: Flight;
  isSelected: boolean;
  onSelect: (id: number) => void;
}

/**
 * Card component displaying flight summary information
 */
export const FlightCard: React.FC<FlightCardProps> = ({ flight, isSelected, onSelect }) => {
  const renderAirlineLogo = (airline: string) => {
    return (
      <div className="w-8 h-8 flex items-center justify-center bg-blue-100 rounded-full text-blue-700 text-xs font-bold">
        {AIRLINES[airline]}
      </div>
    );
  };

  return (
    <div 
      className={`border rounded-lg p-4 cursor-pointer transition-all ${
        isSelected ? 'border-blue-500 bg-blue-50' : 'border-gray-200 hover:border-blue-300'
      }`}
      onClick={() => onSelect(flight.id)}
    >
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          {renderAirlineLogo(flight.airline)}
          <div>
            <div className="font-medium">{flight.airline}</div>
            <div className="text-sm text-gray-500">
              {flight.stops === 0 ? 'Nonstop' : `${flight.stops} stop`} • {flight.duration}
            </div>
          </div>
        </div>
        
        <div className="flex items-center gap-6">
          <div className="text-right mr-2">
            <div className="flex items-center gap-2">
              <Calendar size={16} className="text-gray-500" />
              <span className="text-sm">{flight.date} - {flight.returnDate}</span>
            </div>
            <div className="flex items-center gap-2 mt-1">
              <Clock size={16} className="text-gray-500" />
              <span className="text-sm">{flight.departureTime} - {flight.arrivalTime}</span>
            </div>
          </div>
          
          <div className="flex flex-col items-end">
            <span className="text-lg font-bold text-blue-700">${flight.price}</span>
            <span className="text-xs text-gray-500">round trip</span>
          </div>
          
          {isSelected ? (
            <ChevronUp size={20} className="text-blue-500" />
          ) : (
            <ChevronDown size={20} className="text-gray-400" />
          )}
        </div>
      </div>
    </div>
  );
}; 