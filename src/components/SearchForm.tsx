import React, { useState } from 'react';
import { Search, MapPin, Calendar, Plane, Train, Bus, Loader2 } from 'lucide-react';
import { SearchParams, Trip } from '../types';

interface SearchFormProps {
  onSearch: (params: SearchParams) => Promise<Trip[]>;
  onResults: (trips: Trip[]) => void;
  isLoading: boolean;
}

export const SearchForm: React.FC<SearchFormProps> = ({ onSearch, onResults, isLoading }) => {
  const [searchParams, setSearchParams] = useState<SearchParams>({
    source: '',
    destination: '',
    date: '',
    mode: ''
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const results = await onSearch(searchParams);
    onResults(results);
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    setSearchParams({
      ...searchParams,
      [e.target.name]: e.target.value
    });
  };

  const cities = ['Delhi', 'Mumbai', 'Bangalore', 'Chennai', 'Kolkata', 'Hyderabad', 'Pune', 'Ahmedabad'];

  return (
    <div className="bg-white rounded-2xl shadow-lg p-8 border border-gray-100">
      <div className="flex items-center mb-6">
        <Search className="h-6 w-6 text-blue-600 mr-3" />
        <h2 className="text-2xl font-bold text-gray-900">Search Trips</h2>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="relative">
            <label className="block text-sm font-medium text-gray-700 mb-2">From</label>
            <div className="relative">
              <MapPin className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
              <input
                type="text"
                name="source"
                value={searchParams.source}
                onChange={handleInputChange}
                placeholder="Source city"
                list="cities-from"
                className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors"
              />
              <datalist id="cities-from">
                {cities.map(city => (
                  <option key={city} value={city} />
                ))}
              </datalist>
            </div>
          </div>

          <div className="relative">
            <label className="block text-sm font-medium text-gray-700 mb-2">To</label>
            <div className="relative">
              <MapPin className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
              <input
                type="text"
                name="destination"
                value={searchParams.destination}
                onChange={handleInputChange}
                placeholder="Destination city"
                list="cities-to"
                className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors"
              />
              <datalist id="cities-to">
                {cities.map(city => (
                  <option key={city} value={city} />
                ))}
              </datalist>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="relative">
            <label className="block text-sm font-medium text-gray-700 mb-2">Travel Date</label>
            <div className="relative">
              <Calendar className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
              <input
                type="date"
                name="date"
                value={searchParams.date}
                onChange={handleInputChange}
                min={new Date().toISOString().split('T')[0]}
                className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors"
              />
            </div>
          </div>

          <div className="relative">
            <label className="block text-sm font-medium text-gray-700 mb-2">Travel Mode</label>
            <select
              name="mode"
              value={searchParams.mode}
              onChange={handleInputChange}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors appearance-none bg-white"
            >
              <option value="">All modes</option>
              <option value="flight">Flight</option>
              <option value="train">Train</option>
              <option value="bus">Bus</option>
            </select>
          </div>
        </div>

        <button
          type="submit"
          disabled={isLoading}
          className="w-full bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 text-white font-semibold py-3 px-6 rounded-lg transition-all duration-200 transform hover:scale-[1.02] disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none flex items-center justify-center"
        >
          {isLoading ? (
            <Loader2 className="w-5 h-5 animate-spin mr-2" />
          ) : (
            <Search className="w-5 h-5 mr-2" />
          )}
          {isLoading ? 'Searching...' : 'Search Trips'}
        </button>
      </form>
    </div>
  );
};