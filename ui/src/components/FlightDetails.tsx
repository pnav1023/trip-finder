import React from 'react';
import { Clock, Briefcase, ExternalLink } from 'lucide-react';
import { FlightDetails as FlightDetailsType } from '../types';

interface FlightDetailsProps {
  details: FlightDetailsType;
}

/**
 * Detailed flight information component
 */
export const FlightDetails: React.FC<FlightDetailsProps> = ({ details }) => {
  return (
    <div className="border border-blue-200 rounded-lg bg-blue-50 p-6 my-4 animate-fadeIn">
      <div className="flex justify-between items-start mb-6">
        <div>
          <h3 className="text-xl font-bold text-gray-800">
            {details.departureAirport} → {details.arrivalAirport}
          </h3>
          <p className="text-gray-600">
            {details.departureTime} - {details.arrivalTime} • {details.duration} 
            {details.stops === 0 ? ' • Nonstop' : ` • ${details.stops} Stop`}
          </p>
        </div>
        <div className="text-right">
          <div className="text-2xl font-bold text-blue-700">${details.price}</div>
          <p className="text-sm text-gray-600">round trip per person</p>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-8 mb-6">
        <div>
          <h4 className="text-sm font-semibold text-gray-700 mb-3">OUTBOUND</h4>
          {/* Flight path visualization */}
          <div className="flex justify-between mb-1">
            <div className="font-medium">{details.departureTime}</div>
            <div className="text-gray-600">{details.departureAirport}</div>
          </div>
          <div className="flex items-center py-2">
            <div className="w-1 h-1 rounded-full bg-gray-400"></div>
            <div className="flex-1 h-px bg-gray-300 mx-2"></div>
            <Clock size={14} className="text-gray-500" />
            <div className="mx-2 text-xs text-gray-500">{details.duration}</div>
            <div className="flex-1 h-px bg-gray-300 mx-2"></div>
            <div className="w-1 h-1 rounded-full bg-gray-400"></div>
          </div>
          <div className="flex justify-between mt-1">
            <div className="font-medium">{details.arrivalTime}</div>
            <div className="text-gray-600">{details.arrivalAirport}</div>
          </div>
          {details.stops > 0 && (
            <div className="mt-2 text-sm text-gray-600">
              1 stop in {details.stopLocation}
            </div>
          )}
        </div>

        <div>
          <h4 className="text-sm font-semibold text-gray-700 mb-3">RETURN ({details.returnDate})</h4>
          {/* Return flight path visualization */}
          <div className="flex justify-between mb-1">
            <div className="font-medium">{details.returnDepartureTime}</div>
            <div className="text-gray-600">{details.arrivalAirport}</div>
          </div>
          <div className="flex items-center py-2">
            <div className="w-1 h-1 rounded-full bg-gray-400"></div>
            <div className="flex-1 h-px bg-gray-300 mx-2"></div>
            <Clock size={14} className="text-gray-500" />
            <div className="mx-2 text-xs text-gray-500">{details.returnDuration}</div>
            <div className="flex-1 h-px bg-gray-300 mx-2"></div>
            <div className="w-1 h-1 rounded-full bg-gray-400"></div>
          </div>
          <div className="flex justify-between mt-1">
            <div className="font-medium">{details.returnArrivalTime}</div>
            <div className="text-gray-600">{details.departureAirport}</div>
          </div>
          {details.returnStops > 0 && (
            <div className="mt-2 text-sm text-gray-600">
              1 stop in {details.returnStopLocation}
            </div>
          )}
        </div>
      </div>

      <div className="flex items-center gap-2 mb-6 text-sm text-gray-700">
        <Briefcase size={16} />
        <span>{details.baggage}</span>
      </div>

      <div className="flex justify-end">
        <a 
          href="#book" 
          className="bg-blue-600 text-white px-8 py-3 rounded-lg hover:bg-blue-700 transition-colors flex items-center gap-2"
        >
          Book Flight
          <ExternalLink size={16} />
        </a>
      </div>
    </div>
  );
}; 