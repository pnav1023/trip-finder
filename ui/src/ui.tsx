import { useState } from 'react';
import { Search, Edit2, ChevronDown, ChevronUp, Clock, Briefcase, ExternalLink, Calendar, AlertCircle, Send } from 'lucide-react';

// Mock airline data with logos (using initials as placeholders)
const airlines = {
  "American Airlines": "AA",
  "Delta": "DL",
  "United": "UA",
  "JetBlue": "JB",
  "Southwest": "SW",
  "Alaska": "AS"
};

// Mock flight data generator function
const generateFlights = (refinement = null) => {
  // Base flight options
  const baseFlights = [
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
      price: 265, 
      airline: "American Airlines",
      departureTime: "1:30 PM",
      arrivalTime: "5:12 PM",
      duration: "3h 42m",
      date: "Jun 24",
      returnDate: "Jul 1",
      stops: 0
    },
    { 
      id: 3, 
      price: 275, 
      airline: "Southwest",
      departureTime: "10:20 AM",
      arrivalTime: "1:45 PM",
      duration: "3h 25m",
      date: "Jun 10",
      returnDate: "Jun 17",
      stops: 1
    }
  ];
  
  // For refinements, modify the flights based on input
  if (refinement) {
    if (refinement.toLowerCase().includes('morning')) {
      return [
        { 
          id: 4, 
          price: 255, 
          airline: "Delta",
          departureTime: "6:30 AM",
          arrivalTime: "9:58 AM",
          duration: "3h 28m", 
          date: "Jun 15",
          returnDate: "Jun 22",
          stops: 0
        },
        { 
          id: 5, 
          price: 285, 
          airline: "United",
          departureTime: "8:15 AM",
          arrivalTime: "11:40 AM",
          duration: "3h 25m",
          date: "Jun 16",
          returnDate: "Jun 23",
          stops: 0
        },
        { 
          id: 6, 
          price: 275, 
          airline: "JetBlue",
          departureTime: "7:45 AM",
          arrivalTime: "11:10 AM",
          duration: "3h 25m",
          date: "Jun 14",
          returnDate: "Jun 21",
          stops: 1
        }
      ];
    } else if (refinement.toLowerCase().includes('cheaper') || refinement.toLowerCase().includes('less')) {
      return [
        { 
          id: 7, 
          price: 199, 
          airline: "Southwest",
          departureTime: "5:15 AM",
          arrivalTime: "8:43 AM",
          duration: "3h 28m", 
          date: "Jun 18",
          returnDate: "Jun 25",
          stops: 1
        },
        { 
          id: 8, 
          price: 219, 
          airline: "JetBlue",
          departureTime: "10:30 PM",
          arrivalTime: "2:12 AM",
          duration: "3h 42m",
          date: "Jun 23",
          returnDate: "Jun 30",
          stops: 1
        },
        { 
          id: 9, 
          price: 235, 
          airline: "Delta",
          departureTime: "6:20 AM",
          arrivalTime: "9:45 AM",
          duration: "3h 25m",
          date: "Jun 17",
          returnDate: "Jun 24",
          stops: 1
        }
      ];
    } else if (refinement.toLowerCase().includes('direct') || refinement.toLowerCase().includes('nonstop')) {
      return [
        { 
          id: 10, 
          price: 279, 
          airline: "Delta",
          departureTime: "9:15 AM",
          arrivalTime: "12:43 PM",
          duration: "3h 28m", 
          date: "Jun 14",
          returnDate: "Jun 21",
          stops: 0
        },
        { 
          id: 11, 
          price: 295, 
          airline: "American Airlines",
          departureTime: "2:30 PM",
          arrivalTime: "6:12 PM",
          duration: "3h 42m",
          date: "Jun 15",
          returnDate: "Jun 22",
          stops: 0
        },
        { 
          id: 12, 
          price: 310, 
          airline: "United",
          departureTime: "11:20 AM",
          arrivalTime: "2:45 PM",
          duration: "3h 25m",
          date: "Jun 16",
          returnDate: "Jun 23",
          stops: 0
        }
      ];
    }
  }
  
  return baseFlights;
};

// Mock flight details generator
const generateFlightDetails = (flightId) => {
  const baseDetails = {
    departureAirport: "BOS",
    arrivalAirport: "LAX",
    returnStops: 1,
    returnStopLocation: "DFW",
    baggage: "First bag $30, Second bag $40",
    returnDepartureTime: "8:30 PM",
    returnArrivalTime: "4:55 AM",
    returnDuration: "5h 25m",
  };
  
  // IDs from different refinement generations
  const flightById = {
    1: {
      ...baseDetails,
      departureTime: "7:15 AM",
      arrivalTime: "10:43 AM",
      duration: "3h 28m",
      stops: 0,
      returnDate: "Jun 19",
      price: 245
    },
    2: {
      ...baseDetails,
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
      departureTime: "6:30 AM",
      arrivalTime: "9:58 AM",
      duration: "3h 28m",
      stops: 0,
      returnDate: "Jun 22",
      price: 255
    },
    5: {
      ...baseDetails,
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
      departureTime: "11:20 AM",
      arrivalTime: "2:45 PM",
      duration: "3h 25m",
      stops: 0,
      returnDate: "Jun 23",
      baggage: "First bag $30, Second bag $40",
      price: 310
    },
  };
  
  return flightById[flightId] || flightById[1]; // Default to first flight if not found
};

export default function FlightSearchChatbot() {
  const [prompt, setPrompt] = useState('');
  const [processing, setProcessing] = useState(false);
  const [searchPerformed, setSearchPerformed] = useState(false);
  const [selectedFlight, setSelectedFlight] = useState(null);
  const [conversationHistory, setConversationHistory] = useState([]);
  const [currentFlights, setCurrentFlights] = useState([]);
  const [summaryText, setSummaryText] = useState("");
  
  const handleSearch = () => {
    if (!prompt.trim()) return;
    
    setProcessing(true);
    setSelectedFlight(null);
    
    // Add user message to conversation
    const newHistory = [...conversationHistory, { 
      type: 'user', 
      text: prompt 
    }];
    
    setConversationHistory(newHistory);
    
    // Simulate API call delay
    setTimeout(() => {
      let newFlights;
      let summary;
      
      if (!searchPerformed) {
        // Initial search
        newFlights = generateFlights();
        summary = "Based on your request, here are the best BOS → LAX flights in June:";
        setSummaryText(summary);
      } else {
        // Refinement search
        newFlights = generateFlights(prompt);
        
        // Generate appropriate summary based on refinement
        if (prompt.toLowerCase().includes('morning')) {
          summary = "Showing morning flights only for your BOS → LAX trip:";
        } else if (prompt.toLowerCase().includes('cheaper') || prompt.toLowerCase().includes('less')) {
          summary = "Here are more budget-friendly options for your BOS → LAX trip:";
        } else if (prompt.toLowerCase().includes('direct') || prompt.toLowerCase().includes('nonstop')) {
          summary = "Showing only nonstop flights for your BOS → LAX trip:";
        } else {
          summary = "I've refined your search. Here are updated BOS → LAX flight options:";
        }
        
        setSummaryText(summary);
      }
      
      // Add system response to conversation
      setConversationHistory([...newHistory, {
        type: 'system',
        text: summary,
        flights: newFlights
      }]);
      
      setCurrentFlights(newFlights);
      setProcessing(false);
      setSearchPerformed(true);
      setPrompt('');
    }, 2000);
  };
  
  const handleFlightSelect = (flightId) => {
    if (selectedFlight === flightId) {
      setSelectedFlight(null);
    } else {
      setSelectedFlight(flightId);
    }
  };

  const renderAirlineLogo = (airline) => {
    return (
      <div className="w-8 h-8 flex items-center justify-center bg-blue-100 rounded-full text-blue-700 text-xs font-bold">
        {airlines[airline]}
      </div>
    );
  };
  
  const renderFlightOptions = (flights) => {
    return (
      <div className="space-y-4 mb-6">
        {flights.map((flight) => (
          <div 
            key={flight.id}
            className={`border rounded-lg p-4 cursor-pointer transition-all ${
              selectedFlight === flight.id ? 'border-blue-500 bg-blue-50' : 'border-gray-200 hover:border-blue-300'
            }`}
            onClick={() => handleFlightSelect(flight.id)}
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
                
                {selectedFlight === flight.id ? (
                  <ChevronUp size={20} className="text-blue-500" />
                ) : (
                  <ChevronDown size={20} className="text-gray-400" />
                )}
              </div>
            </div>
          </div>
        ))}
      </div>
    );
  };

  return (
    <div className="max-w-4xl mx-auto p-4 bg-white min-h-screen flex flex-col">
      {/* Initial centered search state */}
      {!searchPerformed && !processing && (
        <div className="flex flex-col items-center justify-center flex-grow">
          <div className="w-full max-w-2xl">
            <h1 className="text-3xl font-bold text-center text-gray-800 mb-8">Find Your Flight</h1>
            <div className="relative">
              <input
                type="text"
                className="w-full p-4 pr-12 border border-gray-300 rounded-lg text-base focus:outline-none focus:ring-2 focus:ring-blue-500 shadow-sm"
                placeholder="Tell me where and when you want to go"
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && prompt.trim() && handleSearch()}
              />
              <button 
                className={`absolute right-3 top-1/2 transform -translate-y-1/2 ${!prompt.trim() ? 'text-gray-400' : 'text-blue-600 cursor-pointer'}`}
                onClick={() => prompt.trim() && handleSearch()}
                disabled={!prompt.trim()}
              >
                <Search size={24} />
              </button>
            </div>
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
              <div key={index} className={`${message.type === 'user' ? 'ml-auto max-w-3xl' : 'mr-auto'}`}>
                {message.type === 'user' ? (
                  <div className="bg-blue-100 text-blue-800 p-3 rounded-lg rounded-tr-none">
                    {message.text}
                  </div>
                ) : (
                  <div>
                    <div className="bg-gray-100 p-3 rounded-lg rounded-tl-none mb-4">
                      {message.text}
                    </div>
                    {message.flights && renderFlightOptions(message.flights)}
                  </div>
                )}
              </div>
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
            <div className="border border-blue-200 rounded-lg bg-blue-50 p-6 my-4 animate-fadeIn">
              <div className="flex justify-between items-start mb-6">
                <div>
                  <h3 className="text-xl font-bold text-gray-800">
                    {generateFlightDetails(selectedFlight).departureAirport} → {generateFlightDetails(selectedFlight).arrivalAirport}
                  </h3>
                  <p className="text-gray-600">
                    {generateFlightDetails(selectedFlight).departureTime} - {generateFlightDetails(selectedFlight).arrivalTime} • {generateFlightDetails(selectedFlight).duration} 
                    {generateFlightDetails(selectedFlight).stops === 0 ? ' • Nonstop' : ` • ${generateFlightDetails(selectedFlight).stops} Stop`}
                  </p>
                </div>
                <div className="text-right">
                  <div className="text-2xl font-bold text-blue-700">${generateFlightDetails(selectedFlight).price}</div>
                  <p className="text-sm text-gray-600">round trip per person</p>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-8 mb-6">
                <div>
                  <h4 className="text-sm font-semibold text-gray-700 mb-3">OUTBOUND</h4>
                  <div className="flex justify-between mb-1">
                    <div className="font-medium">{generateFlightDetails(selectedFlight).departureTime}</div>
                    <div className="text-gray-600">{generateFlightDetails(selectedFlight).departureAirport}</div>
                  </div>
                  <div className="flex items-center py-2">
                    <div className="w-1 h-1 rounded-full bg-gray-400"></div>
                    <div className="flex-1 h-px bg-gray-300 mx-2"></div>
                    <Clock size={14} className="text-gray-500" />
                    <div className="mx-2 text-xs text-gray-500">{generateFlightDetails(selectedFlight).duration}</div>
                    <div className="flex-1 h-px bg-gray-300 mx-2"></div>
                    <div className="w-1 h-1 rounded-full bg-gray-400"></div>
                  </div>
                  <div className="flex justify-between mt-1">
                    <div className="font-medium">{generateFlightDetails(selectedFlight).arrivalTime}</div>
                    <div className="text-gray-600">{generateFlightDetails(selectedFlight).arrivalAirport}</div>
                  </div>
                  {generateFlightDetails(selectedFlight).stops > 0 && (
                    <div className="mt-2 text-sm text-gray-600">
                      1 stop in {generateFlightDetails(selectedFlight).stopLocation}
                    </div>
                  )}
                </div>

                <div>
                  <h4 className="text-sm font-semibold text-gray-700 mb-3">RETURN ({generateFlightDetails(selectedFlight).returnDate})</h4>
                  <div className="flex justify-between mb-1">
                    <div className="font-medium">{generateFlightDetails(selectedFlight).returnDepartureTime}</div>
                    <div className="text-gray-600">{generateFlightDetails(selectedFlight).arrivalAirport}</div>
                  </div>
                  <div className="flex items-center py-2">
                    <div className="w-1 h-1 rounded-full bg-gray-400"></div>
                    <div className="flex-1 h-px bg-gray-300 mx-2"></div>
                    <Clock size={14} className="text-gray-500" />
                    <div className="mx-2 text-xs text-gray-500">{generateFlightDetails(selectedFlight).returnDuration}</div>
                    <div className="flex-1 h-px bg-gray-300 mx-2"></div>
                    <div className="w-1 h-1 rounded-full bg-gray-400"></div>
                  </div>
                  <div className="flex justify-between mt-1">
                    <div className="font-medium">{generateFlightDetails(selectedFlight).returnArrivalTime}</div>
                    <div className="text-gray-600">{generateFlightDetails(selectedFlight).departureAirport}</div>
                  </div>
                  {generateFlightDetails(selectedFlight).returnStops > 0 && (
                    <div className="mt-2 text-sm text-gray-600">
                      1 stop in {generateFlightDetails(selectedFlight).returnStopLocation}
                    </div>
                  )}
                </div>
              </div>

              <div className="flex items-center gap-2 mb-6 text-sm text-gray-700">
                <Briefcase size={16} />
                <span>{generateFlightDetails(selectedFlight).baggage}</span>
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
          )}
          
          {/* Chatbot input */}
          <div className="mt-auto pt-4 border-t border-gray-200">
            <div className="relative">
              <input
                type="text"
                className="w-full p-3 pr-12 border border-gray-300 rounded-lg text-base focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Refine your search (e.g., 'Show me morning flights only')"
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && prompt.trim() && handleSearch()}
                disabled={processing}
              />
              <button 
                className={`absolute right-3 top-1/2 transform -translate-y-1/2 ${processing || !prompt.trim() ? 'text-gray-400' : 'text-blue-600 cursor-pointer'}`}
                onClick={() => prompt.trim() && !processing && handleSearch()}
                disabled={processing || !prompt.trim()}
              >
                <Send size={20} />
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}