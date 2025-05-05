import { useState } from 'react';
import { Flight, ChatMessage } from '../types';
import { generateFlights } from '../data/mockFlightData';

/**
 * Custom hook to manage flight search state and logic
 */
export const useFlightSearch = () => {
  const [prompt, setPrompt] = useState('');
  const [processing, setProcessing] = useState(false);
  const [searchPerformed, setSearchPerformed] = useState(false);
  const [selectedFlight, setSelectedFlight] = useState<number | null>(null);
  const [conversationHistory, setConversationHistory] = useState<ChatMessage[]>([]);
  const [currentFlights, setCurrentFlights] = useState<Flight[]>([]);
  const [summaryText, setSummaryText] = useState('');

  const handleSearch = () => {
    if (!prompt.trim()) return;
    
    setProcessing(true);
    setSelectedFlight(null);
    
    // Add user message to conversation
    const newHistory = [...conversationHistory, { 
      type: 'user' as const, 
      text: prompt 
    }];
    
    setConversationHistory(newHistory);
    
    // Simulate API call delay
    setTimeout(async () => {
      let newFlights: Flight[];
      let summary: string;
      
      if (!searchPerformed) {
        // Initial search
        newFlights = await generateFlights();
        summary = "Based on your request, here are the best BOS → LAX flights in June:";
      } else {
        // Refinement search
        newFlights = await generateFlights(prompt);
        
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
      }
      
      setSummaryText(summary);
      
      // Add system response to conversation
      setConversationHistory([...newHistory, {
        type: 'system' as const,
        text: summary,
        flights: newFlights
      }]);
      
      setCurrentFlights(newFlights);
      setProcessing(false);
      setSearchPerformed(true);
      setPrompt('');
    }, 2000);
  };

  const handleFlightSelect = (flightId: number) => {
    if (selectedFlight === flightId) {
      setSelectedFlight(null);
    } else {
      setSelectedFlight(flightId);
    }
  };

  return {
    prompt,
    setPrompt,
    processing,
    searchPerformed,
    selectedFlight,
    conversationHistory,
    currentFlights,
    summaryText,
    handleSearch,
    handleFlightSelect
  };
}; 