export interface User {
  id: string;
  name: string;
  email: string;
  isAdmin?: boolean;
}

export interface Trip {
  id: string;
  source: string;
  destination: string;
  date: string;
  price: number;
  mode: 'flight' | 'train' | 'bus';
  duration: string;
  departureTime: string;
  arrivalTime: string;
  availableSeats: number;
}

export interface Booking {
  id: string;
  userId: string;
  tripId: string;
  bookingDate: string;
  status: 'confirmed' | 'pending' | 'cancelled';
  passengers: number;
  totalAmount: number;
  trip: Trip;
}

export interface SearchParams {
  source: string;
  destination: string;
  date: string;
  mode?: string;
}