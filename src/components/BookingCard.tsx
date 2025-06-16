import React from 'react';
import { Plane, Train, Bus, Calendar, Users, MapPin, Clock, CreditCard } from 'lucide-react';
import { Booking } from '../types';

interface BookingCardProps {
  booking: Booking;
  onCancel?: (bookingId: string) => void;
}

export const BookingCard: React.FC<BookingCardProps> = ({ booking, onCancel }) => {
  const getModeIcon = () => {
    switch (booking.trip.mode) {
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

  const getStatusColor = () => {
    switch (booking.status) {
      case 'confirmed':
        return 'bg-green-100 text-green-700 border-green-200';
      case 'pending':
        return 'bg-yellow-100 text-yellow-700 border-yellow-200';
      case 'cancelled':
        return 'bg-red-100 text-red-700 border-red-200';
      default:
        return 'bg-gray-100 text-gray-700 border-gray-200';
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      weekday: 'short',
      month: 'short',
      day: 'numeric',
      year: 'numeric'
    });
  };

  const formatDateTime = (dateString: string) => {
    return new Date(dateString).toLocaleString('en-US', {
      month: 'short',
      day: 'numeric',
      hour: 'numeric',
      minute: '2-digit'
    });
  };

  return (
    <div className="bg-white rounded-xl shadow-md border border-gray-100 overflow-hidden">
      <div className="p-6">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center space-x-3">
            {getModeIcon()}
            <div>
              <div className="font-semibold text-gray-900">Booking #{booking.id.slice(-6)}</div>
              <div className="text-sm text-gray-500">Booked on {formatDateTime(booking.bookingDate)}</div>
            </div>
          </div>
          <span className={`px-3 py-1 rounded-full text-sm font-medium border ${getStatusColor()}`}>
            {booking.status.charAt(0).toUpperCase() + booking.status.slice(1)}
          </span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
          <div className="flex items-center space-x-2">
            <MapPin className="h-4 w-4 text-gray-400" />
            <div>
              <div className="font-semibold text-gray-900">{booking.trip.source}</div>
              <div className="text-sm text-gray-500">{booking.trip.departureTime}</div>
            </div>
          </div>

          <div className="flex items-center justify-center">
            <div className="text-center">
              <Clock className="h-4 w-4 text-gray-400 mx-auto mb-1" />
              <div className="text-sm font-medium text-gray-700">{booking.trip.duration}</div>
            </div>
          </div>

          <div className="flex items-center space-x-2 justify-end">
            <div className="text-right">
              <div className="font-semibold text-gray-900">{booking.trip.destination}</div>
              <div className="text-sm text-gray-500">{booking.trip.arrivalTime}</div>
            </div>
            <MapPin className="h-4 w-4 text-gray-400" />
          </div>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
          <div className="flex items-center space-x-2">
            <Calendar className="h-4 w-4 text-gray-400" />
            <div className="text-sm">
              <div className="text-gray-500">Travel Date</div>
              <div className="font-medium text-gray-900">{formatDate(booking.trip.date)}</div>
            </div>
          </div>

          <div className="flex items-center space-x-2">
            <Users className="h-4 w-4 text-gray-400" />
            <div className="text-sm">
              <div className="text-gray-500">Passengers</div>
              <div className="font-medium text-gray-900">{booking.passengers}</div>
            </div>
          </div>

          <div className="flex items-center space-x-2">
            <CreditCard className="h-4 w-4 text-gray-400" />
            <div className="text-sm">
              <div className="text-gray-500">Total Amount</div>
              <div className="font-bold text-gray-900">₹{booking.totalAmount.toLocaleString()}</div>
            </div>
          </div>

          <div className="flex items-center space-x-2">
            <div className="w-4 h-4 rounded-full bg-gray-400"></div>
            <div className="text-sm">
              <div className="text-gray-500">Mode</div>
              <div className="font-medium text-gray-900 capitalize">{booking.trip.mode}</div>
            </div>
          </div>
        </div>

        {booking.status === 'confirmed' && onCancel && (
          <div className="border-t pt-4">
            <button
              onClick={() => onCancel(booking.id)}
              className="bg-red-100 hover:bg-red-200 text-red-700 font-medium py-2 px-4 rounded-lg transition-colors text-sm"
            >
              Cancel Booking
            </button>
          </div>
        )}
      </div>
    </div>
  );
};