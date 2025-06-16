import sqlite3
import hashlib
from datetime import datetime, date
import os

class DatabaseManager:
    def __init__(self, db_name="travel_booking.db"):
        self.db_name = db_name
        self.init_database()
    
    def get_connection(self):
        """Get database connection"""
        return sqlite3.connect(self.db_name)
    
    def init_database(self):
        """Initialize database with required tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Create users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                is_admin BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create trips table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS trips (
                trip_id INTEGER PRIMARY KEY AUTOINCREMENT,
                source TEXT NOT NULL,
                destination TEXT NOT NULL,
                date DATE NOT NULL,
                price REAL NOT NULL,
                mode TEXT NOT NULL CHECK(mode IN ('flight', 'train', 'bus')),
                duration TEXT NOT NULL,
                departure_time TEXT NOT NULL,
                arrival_time TEXT NOT NULL,
                available_seats INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create bookings table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bookings (
                booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                trip_id INTEGER NOT NULL,
                passengers INTEGER DEFAULT 1,
                total_amount REAL NOT NULL,
                booking_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'confirmed' CHECK(status IN ('confirmed', 'cancelled', 'pending')),
                FOREIGN KEY (user_id) REFERENCES users (user_id),
                FOREIGN KEY (trip_id) REFERENCES trips (trip_id)
            )
        ''')
        
        # Insert sample admin user
        cursor.execute('''
            INSERT OR IGNORE INTO users (name, email, password, is_admin)
            VALUES ('Admin User', 'admin@travel.com', ?, 1)
        ''', (self.hash_password('admin123'),))
        
        # Insert sample trips
        sample_trips = [
            ('Delhi', 'Mumbai', '2025-01-25', 5500.0, 'flight', '2h 15m', '06:00', '08:15', 45),
            ('Delhi', 'Mumbai', '2025-01-25', 1200.0, 'train', '16h 30m', '22:30', '15:00', 120),
            ('Mumbai', 'Bangalore', '2025-01-26', 4200.0, 'flight', '1h 45m', '14:30', '16:15', 30),
            ('Delhi', 'Bangalore', '2025-01-27', 800.0, 'bus', '24h 00m', '20:00', '20:00', 25),
            ('Chennai', 'Kolkata', '2025-01-28', 6200.0, 'flight', '2h 30m', '09:15', '11:45', 60),
            ('Bangalore', 'Chennai', '2025-01-29', 3800.0, 'flight', '1h 30m', '11:00', '12:30', 50),
            ('Mumbai', 'Delhi', '2025-01-30', 5200.0, 'flight', '2h 10m', '16:45', '18:55', 40),
            ('Kolkata', 'Delhi', '2025-01-31', 900.0, 'train', '17h 15m', '18:30', '11:45', 100)
        ]
        
        cursor.executemany('''
            INSERT OR IGNORE INTO trips 
            (source, destination, date, price, mode, duration, departure_time, arrival_time, available_seats)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', sample_trips)
        
        conn.commit()
        conn.close()
    
    def hash_password(self, password):
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def register_user(self, name, email, password):
        """Register a new user"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            hashed_password = self.hash_password(password)
            cursor.execute('''
                INSERT INTO users (name, email, password)
                VALUES (?, ?, ?)
            ''', (name, email, hashed_password))
            
            conn.commit()
            conn.close()
            return True, "User registered successfully"
        except sqlite3.IntegrityError:
            return False, "Email already exists"
        except Exception as e:
            return False, f"Registration failed: {str(e)}"
    
    def login_user(self, email, password):
        """Authenticate user login"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        hashed_password = self.hash_password(password)
        cursor.execute('''
            SELECT user_id, name, email, is_admin FROM users
            WHERE email = ? AND password = ?
        ''', (email, hashed_password))
        
        user = cursor.fetchone()
        conn.close()
        
        if user:
            return True, {
                'user_id': user[0],
                'name': user[1],
                'email': user[2],
                'is_admin': user[3]
            }
        return False, "Invalid credentials"
    
    def search_trips(self, source=None, destination=None, date=None, mode=None):
        """Search for trips based on criteria"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = "SELECT * FROM trips WHERE available_seats > 0"
        params = []
        
        if source:
            query += " AND LOWER(source) LIKE LOWER(?)"
            params.append(f"%{source}%")
        
        if destination:
            query += " AND LOWER(destination) LIKE LOWER(?)"
            params.append(f"%{destination}%")
        
        if date:
            query += " AND date = ?"
            params.append(date)
        
        if mode:
            query += " AND mode = ?"
            params.append(mode)
        
        query += " ORDER BY date, departure_time"
        
        cursor.execute(query, params)
        trips = cursor.fetchall()
        conn.close()
        
        return trips
    
    def book_trip(self, user_id, trip_id, passengers=1):
        """Book a trip for a user"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Get trip details
            cursor.execute("SELECT price, available_seats FROM trips WHERE trip_id = ?", (trip_id,))
            trip = cursor.fetchone()
            
            if not trip:
                return False, "Trip not found"
            
            price, available_seats = trip
            
            if available_seats < passengers:
                return False, "Not enough seats available"
            
            total_amount = price * passengers
            
            # Create booking
            cursor.execute('''
                INSERT INTO bookings (user_id, trip_id, passengers, total_amount)
                VALUES (?, ?, ?, ?)
            ''', (user_id, trip_id, passengers, total_amount))
            
            # Update available seats
            cursor.execute('''
                UPDATE trips SET available_seats = available_seats - ?
                WHERE trip_id = ?
            ''', (passengers, trip_id))
            
            conn.commit()
            conn.close()
            return True, "Booking successful"
        except Exception as e:
            return False, f"Booking failed: {str(e)}"
    
    def get_user_bookings(self, user_id):
        """Get all bookings for a user"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT b.booking_id, b.passengers, b.total_amount, b.booking_date, b.status,
                   t.source, t.destination, t.date, t.mode, t.departure_time, t.arrival_time, t.duration
            FROM bookings b
            JOIN trips t ON b.trip_id = t.trip_id
            WHERE b.user_id = ?
            ORDER BY b.booking_date DESC
        ''', (user_id,))
        
        bookings = cursor.fetchall()
        conn.close()
        return bookings
    
    def get_all_bookings(self):
        """Get all bookings (admin only)"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT b.booking_id, u.name, u.email, b.passengers, b.total_amount, 
                   b.booking_date, b.status, t.source, t.destination, t.date, t.mode
            FROM bookings b
            JOIN users u ON b.user_id = u.user_id
            JOIN trips t ON b.trip_id = t.trip_id
            ORDER BY b.booking_date DESC
        ''')
        
        bookings = cursor.fetchall()
        conn.close()
        return bookings
    
    def add_trip(self, source, destination, date, price, mode, duration, departure_time, arrival_time, available_seats):
        """Add a new trip (admin only)"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO trips (source, destination, date, price, mode, duration, departure_time, arrival_time, available_seats)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (source, destination, date, price, mode, duration, departure_time, arrival_time, available_seats))
            
            conn.commit()
            conn.close()
            return True, "Trip added successfully"
        except Exception as e:
            return False, f"Failed to add trip: {str(e)}"
    
    def delete_trip(self, trip_id):
        """Delete a trip (admin only)"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Check if trip has bookings
            cursor.execute("SELECT COUNT(*) FROM bookings WHERE trip_id = ?", (trip_id,))
            booking_count = cursor.fetchone()[0]
            
            if booking_count > 0:
                return False, "Cannot delete trip with existing bookings"
            
            cursor.execute("DELETE FROM trips WHERE trip_id = ?", (trip_id,))
            conn.commit()
            conn.close()
            return True, "Trip deleted successfully"
        except Exception as e:
            return False, f"Failed to delete trip: {str(e)}"
    
    def cancel_booking(self, booking_id, user_id):
        """Cancel a booking"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Get booking details
            cursor.execute('''
                SELECT trip_id, passengers FROM bookings 
                WHERE booking_id = ? AND user_id = ? AND status = 'confirmed'
            ''', (booking_id, user_id))
            
            booking = cursor.fetchone()
            if not booking:
                return False, "Booking not found or already cancelled"
            
            trip_id, passengers = booking
            
            # Update booking status
            cursor.execute('''
                UPDATE bookings SET status = 'cancelled'
                WHERE booking_id = ?
            ''', (booking_id,))
            
            # Return seats to trip
            cursor.execute('''
                UPDATE trips SET available_seats = available_seats + ?
                WHERE trip_id = ?
            ''', (passengers, trip_id))
            
            conn.commit()
            conn.close()
            return True, "Booking cancelled successfully"
        except Exception as e:
            return False, f"Failed to cancel booking: {str(e)}"