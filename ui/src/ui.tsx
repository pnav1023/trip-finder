import React from 'react';
import { useFlightSearch } from './hooks/useFlightSearch';
import { SearchInput } from './components/SearchInput';
import { ChatMessage } from './components/ChatMessage';
import { FlightDetails } from './components/FlightDetails';
import { generateFlightDetails } from './data/mockFlightData';

/**
 * Main flight search chatbot component
 */
export default function FlightSearchChatbot() {
  const {
    prompt,
    setPrompt,
    processing,
    searchPerformed,
    selectedFlight,
    conversationHistory,
    handleSearch,
    handleFlightSelect
  } = useFlightSearch();

  return (
    <div className="max-w-4xl mx-auto p-4 bg-white min-h-screen flex flex-col">
      {/* Initial centered search state */}
      {!searchPerformed && !processing && (
        <div className="flex flex-col items-center justify-center flex-grow">
          <div className="w-full max-w-2xl">
            <h1 className="text-3xl font-bold text-center text-gray-800 mb-8">Find Your Flight</h1>
            <SearchInput
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              onSearch={handleSearch}
              isProcessing={processing}
              isInitial={true}
            />
            <p className="text-center text-gray-500 mt-4">
              Example: "I want to fly from Boston to LA in June for about a week"
            </p>
          </div>
        </div>
      )}

      {/* Conversation history and search results */}
      {(searchPerformed || processing) && (
        <div className="flex flex-col">
          {/* Chat history */}
          <div className="space-y-6 mb-6">
            {conversationHistory.map((message, index) => (
              <ChatMessage
                key={index}
                message={message}
                selectedFlight={selectedFlight}
                onFlightSelect={handleFlightSelect}
              />
            ))}
            
            {/* Processing indicator */}
            {processing && (
              <div className="flex items-center gap-2 text-gray-600">
                <div className="flex gap-1">
                  {[...Array(3)].map((_, i) => (
                    <div 
                      key={i} 
                      className="w-2 h-2 rounded-full bg-gray-400 animate-pulse"
                      style={{ animationDelay: `${i * 0.15}s` }}
                    ></div>
                  ))}
                </div>
                <span>Searching for flights...</span>
              </div>
            )}
          </div>
          
          {/* Selected flight details */}
          {selectedFlight && (
            <FlightDetails details={generateFlightDetails(selectedFlight)} />
          )}
          
          {/* Chatbot input */}
          <div className="mt-auto pt-4 border-t border-gray-200">
            <SearchInput
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              onSearch={handleSearch}
              isProcessing={processing}
              isInitial={false}
              placeholder="Refine your search (e.g., 'Show me morning flights only')"
            />
          </div>
        </div>
      )}
    </div>
  );
}