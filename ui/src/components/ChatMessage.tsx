import React from 'react';
import { ChatMessage as ChatMessageType, Flight } from '../types';
import { FlightCard } from './FlightCard';

interface ChatMessageProps {
  message: ChatMessageType;
  selectedFlight: number | null;
  onFlightSelect: (id: number) => void;
}

/**
 * Component for rendering a chat message with optional flight results
 */
export const ChatMessage: React.FC<ChatMessageProps> = ({ 
  message, 
  selectedFlight, 
  onFlightSelect 
}) => {
  return (
    <div className={`${message.type === 'user' ? 'ml-auto max-w-3xl' : 'mr-auto'}`}>
      {message.type === 'user' ? (
        <div className="bg-blue-100 text-blue-800 p-3 rounded-lg rounded-tr-none">
          {message.text}
        </div>
      ) : (
        <div>
          <div className="bg-gray-100 p-3 rounded-lg rounded-tl-none mb-4">
            {message.text}
          </div>
          {message.flights && (
            <div className="space-y-4 mb-6">
              {message.flights.map((flight) => (
                <FlightCard
                  key={flight.id}
                  flight={flight}
                  isSelected={selectedFlight === flight.id}
                  onSelect={onFlightSelect}
                />
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}; 