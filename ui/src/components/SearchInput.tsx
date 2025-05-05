import React from 'react';
import { Search, Send } from 'lucide-react';

interface SearchInputProps {
  value: string;
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  onSearch: () => void;
  isProcessing: boolean;
  isInitial?: boolean;
  placeholder?: string;
}

/**
 * Search input component for flight queries
 */
export const SearchInput: React.FC<SearchInputProps> = ({
  value,
  onChange,
  onSearch,
  isProcessing,
  isInitial = false,
  placeholder = "Tell me where and when you want to go"
}) => {
  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && value.trim() && !isProcessing) {
      onSearch();
    }
  };

  const icon = isInitial ? (
    <Search size={24} />
  ) : (
    <Send size={20} />
  );

  return (
    <div className="relative">
      <input
        type="text"
        className={`w-full p-${isInitial ? '4' : '3'} pr-12 border border-gray-300 rounded-lg text-base focus:outline-none focus:ring-2 focus:ring-blue-500 ${isInitial ? 'shadow-sm' : ''}`}
        placeholder={placeholder}
        value={value}
        onChange={onChange}
        onKeyDown={handleKeyDown}
        disabled={isProcessing}
      />
      <button 
        className={`absolute right-3 top-1/2 transform -translate-y-1/2 ${isProcessing || !value.trim() ? 'text-gray-400' : 'text-blue-600 cursor-pointer'}`}
        onClick={() => value.trim() && !isProcessing && onSearch()}
        disabled={isProcessing || !value.trim()}
      >
        {icon}
      </button>
    </div>
  );
}; 