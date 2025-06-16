import React, { useState } from 'react';
import { Plane, Train, Bus, Clock, Users, MapPin, Loader2 } from 'lucide-react';
import { Trip } from '../types';

interface TripCardProps {
  trip: Trip;
  onBook: (tripId: string) => Promise<boolean>;
  isBooking: boolean;
}

export const TripCard: React.FC<TripCardProps> = ({ trip, onBook, isBooking }) => {
  const [passengers, setPassengers] = useState(1);
  const [showBooking, setShowBooking] = useState(false);

  const getModeIcon = () => {
    switch (trip.mode) {
      case 'flight':
        return <Plane className="h-5 w-5 text-blue-600" />;
      case 'train':
        return <Train className="h-5 w-5 text-green-600" />;
      case 'bus':
        return <Bus className="h-5 w-5 text-orange-600" />;
      default:
        return null;
    }
  };

  const getModeColor = () => {
    switch (trip.mode) {
      case 'flight':
        return 'bg-blue-100 text-blue-700 border-blue-200';
      case 'train':
        return 'bg-green-100 text-green-700 border-green-200';
      case 'bus':
        return 'bg-orange-100 text-orange-700 border-orange-200';
      default:
        return 'bg-gray-100 text-gray-700 border-gray-200';
    }
  };

  const handleBook = async () => {
    const success = await onBook(trip.id);
    if (success) {
      setShowBooking(false);
      setPassengers(1);
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      weekday: 'short',
      month: 'short',
      day: 'numeric'
    });
  };

  return (
    <div className="bg-white rounded-xl shadow-md hover:shadow-lg transition-all duration-300 border border-gray-100 overflow-hidden">
      <div className="p-6">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center space-x-3">
            {getModeIcon()}
            <span className={`px-3 py-1 rounded-full text-sm font-medium border ${getModeColor()}`}>
              {trip.mode.charAt(0).toUpperCase() + trip.mode.slice(1)}
            </span>
          </div>
          <div className="text-right">
            <div className="text-2xl font-bold text-gray-900">₹{trip.price.toLocaleString()}</div>
            <div className="text-sm text-gray-500">per person</div>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
          <div className="flex items-center space-x-2">
            <MapPin className="h-4 w-4 text-gray-400" />
            <div>
              <div className="font-semibold text-gray-900">{trip.source}</div>
              <div className="text-sm text-gray-500">{trip.departureTime}</div>
            </div>
          </div>

          <div className="flex items-center justify-center">
            <div className="text-center">
              <Clock className="h-4 w-4 text-gray-400 mx-auto mb-1" />
              <div className="text-sm font-medium text-gray-700">{trip.duration}</div>
            </div>
          </div>

          <div className="flex items-center space-x-2 justify-end">
            <div className="text-right">
              <div className="font-semibold text-gray-900">{trip.destination}</div>
              <div className="text-sm text-gray-500">{trip.arrivalTime}</div>
            </div>
            <MapPin className="h-4 w-4 text-gray-400" />
          </div>
        </div>

        <div className="flex items-center justify-between mb-4">
          <div className="text-sm text-gray-600">
            {formatDate(trip.date)}
          </div>
          <div className="flex items-center space-x-2 text-sm text-gray-600">
            <Users className="h-4 w-4" />
            <span>{trip.availableSeats} seats available</span>
          </div>
        </div>

        {!showBooking ? (
          <button
            onClick={() => setShowBooking(true)}
            disabled={trip.availableSeats === 0}
            className="w-full bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 text-white font-semibold py-3 px-4 rounded-lg transition-all duration-200 transform hover:scale-[1.02] disabled:bg-gray-400 disabled:cursor-not-allowed disabled:transform-none"
          >
            {trip.availableSeats === 0 ? 'Sold Out' : 'Book Now'}
          </button>
        ) : (
          <div className="border-t pt-4 space-y-4">
            <div className="flex items-center justify-between">
              <label className="text-sm font-medium text-gray-700">Passengers:</label>
              <select
                value={passengers}
                onChange={(e) => setPassengers(parseInt(e.target.value))}
                className="border border-gray-300 rounded px-3 py-1 text-sm"
              >
                {[...Array(Math.min(trip.availableSeats, 6))].map((_, i) => (
                  <option key={i + 1} value={i + 1}>{i + 1}</option>
                ))}
              </select>
            </div>
            
            <div className="flex items-center justify-between text-sm">
              <span>Total Amount:</span>
              <span className="font-bold text-lg">₹{(trip.price * passengers).toLocaleString()}</span>
            </div>

            <div className="flex space-x-3">
              <button
                onClick={() => setShowBooking(false)}
                className="flex-1 bg-gray-200 hover:bg-gray-300 text-gray-700 font-medium py-2 px-4 rounded-lg transition-colors"
              >
                Cancel
              </button>
              <button
                onClick={handleBook}
                disabled={isBooking}
                className="flex-1 bg-gradient-to-r from-green-600 to-green-700 hover:from-green-700 hover:to-green-800 text-white font-semibold py-2 px-4 rounded-lg transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
              >
                {isBooking ? (
                  <Loader2 className="w-4 h-4 animate-spin" />
                ) : (
                  'Confirm Booking'
                )}
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};