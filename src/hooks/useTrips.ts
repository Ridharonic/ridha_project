import { useState, useEffect } from 'react';
import { Trip, SearchParams } from '../types';

const SAMPLE_TRIPS: Trip[] = [
  {
    id: '1',
    source: 'Delhi',
    destination: 'Mumbai',
    date: '2025-01-20',
    price: 5500,
    mode: 'flight',
    duration: '2h 15m',
    departureTime: '06:00',
    arrivalTime: '08:15',
    availableSeats: 45
  },
  {
    id: '2',
    source: 'Delhi',
    destination: 'Mumbai',
    date: '2025-01-20',
    price: 1200,
    mode: 'train',
    duration: '16h 30m',
    departureTime: '22:30',
    arrivalTime: '15:00',
    availableSeats: 120
  },
  {
    id: '3',
    source: 'Mumbai',
    destination: 'Bangalore',
    date: '2025-01-21',
    price: 4200,
    mode: 'flight',
    duration: '1h 45m',
    departureTime: '14:30',
    arrivalTime: '16:15',
    availableSeats: 30
  },
  {
    id: '4',
    source: 'Delhi',
    destination: 'Bangalore',
    date: '2025-01-22',
    price: 800,
    mode: 'bus',
    duration: '24h 00m',
    departureTime: '20:00',
    arrivalTime: '20:00',
    availableSeats: 25
  },
  {
    id: '5',
    source: 'Chennai',
    destination: 'Kolkata',
    date: '2025-01-23',
    price: 6200,
    mode: 'flight',
    duration: '2h 30m',
    departureTime: '09:15',
    arrivalTime: '11:45',
    availableSeats: 60
  }
];

export const useTrips = () => {
  const [trips, setTrips] = useState<Trip[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    // Initialize with sample data
    const savedTrips = localStorage.getItem('trips');
    if (savedTrips) {
      setTrips(JSON.parse(savedTrips));
    } else {
      setTrips(SAMPLE_TRIPS);
      localStorage.setItem('trips', JSON.stringify(SAMPLE_TRIPS));
    }
  }, []);

  const searchTrips = async (params: SearchParams): Promise<Trip[]> => {
    setIsLoading(true);
    try {
      // Simulate API delay
      await new Promise(resolve => setTimeout(resolve, 800));
      
      const allTrips = JSON.parse(localStorage.getItem('trips') || '[]');
      const filtered = allTrips.filter((trip: Trip) => {
        const matchesSource = !params.source || trip.source.toLowerCase().includes(params.source.toLowerCase());
        const matchesDestination = !params.destination || trip.destination.toLowerCase().includes(params.destination.toLowerCase());
        const matchesDate = !params.date || trip.date === params.date;
        const matchesMode = !params.mode || trip.mode === params.mode;
        
        return matchesSource && matchesDestination && matchesDate && matchesMode;
      });
      
      return filtered;
    } finally {
      setIsLoading(false);
    }
  };

  const addTrip = (trip: Omit<Trip, 'id'>) => {
    const newTrip = {
      ...trip,
      id: Date.now().toString()
    };
    const updatedTrips = [...trips, newTrip];
    setTrips(updatedTrips);
    localStorage.setItem('trips', JSON.stringify(updatedTrips));
  };

  const deleteTrip = (tripId: string) => {
    const updatedTrips = trips.filter(trip => trip.id !== tripId);
    setTrips(updatedTrips);
    localStorage.setItem('trips', JSON.stringify(updatedTrips));
  };

  return {
    trips,
    searchTrips,
    addTrip,
    deleteTrip,
    isLoading
  };
};