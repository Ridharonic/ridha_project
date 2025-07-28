import React, { useState } from 'react';
import { Search, User, Settings, LogOut, Calendar, Plane, BarChart3, Users } from 'lucide-react';
import { useAuth } from '../hooks/useAuth';
import { useTrips } from '../hooks/useTrips';
import { useBookings } from '../hooks/useBookings';
import { SearchForm } from './SearchForm';
import { TripCard } from './TripCard';
import { BookingCard } from './BookingCard';
import { AdminPanel } from './AdminPanel';
import { Trip } from '../types';

export const Dashboard: React.FC = () => {
  const { user, logout } = useAuth();
  const { searchTrips, isLoading: tripsLoading } = useTrips();
  const { createBooking, getUserBookings, cancelBooking, isLoading: bookingLoading } = useBookings();
  
  const [activeTab, setActiveTab] = useState('search');
  const [searchResults, setSearchResults] = useState<Trip[]>([]);
  const [searchPerformed, setSearchPerformed] = useState(true);

  const userBookings = getUserBookings(user?.id || '');

  // Load all trips when component mounts
  React.useEffect(() => {
    const loadAllTrips = async () => {
      const allTrips = await searchTrips({
        source: '',
        destination: '',
        date: '',
        mode: ''
      });
      setSearchResults(allTrips);
    };
    
    if (activeTab === 'search') {
      loadAllTrips();
    }
  }, [activeTab, searchTrips]);
  const handleSearch = async (params: any) => {
    setSearchPerformed(true);
    const results = await searchTrips(params);
    setSearchResults(results);
    return results;
  };

  const handleBookTrip = async (tripId: string) => {
    if (!user) return false;
    const success = await createBooking(tripId, user.id);
    if (success) {
      // Refresh search results to show updated seat availability
      if (searchPerformed) {
        setSearchResults(prev => prev.map(trip => 
          trip.id === tripId 
            ? { ...trip, availableSeats: trip.availableSeats - 1 }
            : trip
        ));
      }
    }
    return success;
  };

  const tabs = [
    { id: 'search', label: 'Search Trips', icon: Search },
    { id: 'bookings', label: 'My Bookings', icon: Calendar },
    ...(user?.isAdmin ? [{ id: 'admin', label: 'Admin Panel', icon: BarChart3 }] : [])
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center space-x-3">
              <Plane className="h-8 w-8 text-blue-600" />
              <h1 className="text-2xl font-bold text-gray-900">TravelBook</h1>
            </div>
            
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2 text-gray-700">
                <User className="h-5 w-5" />
                <span className="font-medium">{user?.name}</span>
                {user?.isAdmin && (
                  <span className="bg-blue-100 text-blue-700 text-xs px-2 py-1 rounded-full">Admin</span>
                )}
              </div>
              <button
                onClick={logout}
                className="flex items-center space-x-2 text-gray-500 hover:text-gray-700 transition-colors"
              >
                <LogOut className="h-5 w-5" />
                <span>Logout</span>
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Navigation Tabs */}
      <nav className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex space-x-8">
            {tabs.map((tab) => {
              const Icon = tab.icon;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`py-4 px-1 border-b-2 font-medium text-sm flex items-center space-x-2 transition-colors ${
                    activeTab === tab.id
                      ? 'border-blue-500 text-blue-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }`}
                >
                  <Icon className="h-4 w-4" />
                  <span>{tab.label}</span>
                </button>
              );
            })}
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {activeTab === 'search' && (
          <div className="space-y-8">
            <SearchForm
              onSearch={handleSearch}
              onResults={setSearchResults}
              isLoading={tripsLoading}
            />
            
            {searchPerformed && (
              <div>
                <h3 className="text-xl font-semibold text-gray-900 mb-6">
                  {searchResults.length > 0 
                    ? `${searchResults.length} trip${searchResults.length !== 1 ? 's' : ''} available`
                    : 'No trips available'
                  }
                </h3>
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                  {searchResults.map((trip) => (
                    <TripCard
                      key={trip.id}
                      trip={trip}
                      onBook={handleBookTrip}
                      isBooking={bookingLoading}
                    />
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {activeTab === 'bookings' && (
          <div className="space-y-6">
            <div className="flex items-center justify-between">
              <h2 className="text-2xl font-bold text-gray-900">My Bookings</h2>
              <div className="flex items-center space-x-2 text-gray-600">
                <Calendar className="h-5 w-5" />
                <span>{userBookings.length} booking{userBookings.length !== 1 ? 's' : ''}</span>
              </div>
            </div>
            
            {userBookings.length === 0 ? (
              <div className="text-center py-12">
                <Calendar className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                <h3 className="text-lg font-medium text-gray-900 mb-2">No bookings yet</h3>
                <p className="text-gray-500">Start planning your next adventure!</p>
                <button
                  onClick={() => setActiveTab('search')}
                  className="mt-4 bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-lg transition-colors"
                >
                  Search Trips
                </button>
              </div>
            ) : (
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {userBookings.map((booking) => (
                  <BookingCard
                    key={booking.id}
                    booking={booking}
                    onCancel={cancelBooking}
                  />
                ))}
              </div>
            )}
          </div>
        )}

        {activeTab === 'admin' && user?.isAdmin && (
          <AdminPanel />
        )}
      </main>
    </div>
  );
};