import { useState, useEffect } from 'react';
import { Booking, Trip } from '../types';

export const useBookings = () => {
  const [bookings, setBookings] = useState<Booking[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    const savedBookings = localStorage.getItem('bookings');
    if (savedBookings) {
      setBookings(JSON.parse(savedBookings));
    }
  }, []);

  const createBooking = async (tripId: string, userId: string, passengers: number = 1): Promise<boolean> => {
    setIsLoading(true);
    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      const trips = JSON.parse(localStorage.getItem('trips') || '[]');
      const trip = trips.find((t: Trip) => t.id === tripId);
      
      if (!trip || trip.availableSeats < passengers) {
        return false;
      }
      
      const newBooking: Booking = {
        id: Date.now().toString(),
        userId,
        tripId,
        bookingDate: new Date().toISOString(),
        status: 'confirmed',
        passengers,
        totalAmount: trip.price * passengers,
        trip
      };
      
      const updatedBookings = [...bookings, newBooking];
      setBookings(updatedBookings);
      localStorage.setItem('bookings', JSON.stringify(updatedBookings));
      
      // Update available seats
      trip.availableSeats -= passengers;
      const updatedTrips = trips.map((t: Trip) => t.id === tripId ? trip : t);
      localStorage.setItem('trips', JSON.stringify(updatedTrips));
      
      return true;
    } finally {
      setIsLoading(false);
    }
  };

  const getUserBookings = (userId: string): Booking[] => {
    return bookings.filter(booking => booking.userId === userId);
  };

  const getAllBookings = (): Booking[] => {
    return bookings;
  };

  const cancelBooking = (bookingId: string) => {
    const updatedBookings = bookings.map(booking => 
      booking.id === bookingId 
        ? { ...booking, status: 'cancelled' as const }
        : booking
    );
    setBookings(updatedBookings);
    localStorage.setItem('bookings', JSON.stringify(updatedBookings));
  };

  return {
    createBooking,
    getUserBookings,
    getAllBookings,
    cancelBooking,
    isLoading
  };
};