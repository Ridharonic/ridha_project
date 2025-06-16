import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, date
from db import DatabaseManager

class AdminPanel:
    def __init__(self, parent_frame, user_data):
        self.parent_frame = parent_frame
        self.user_data = user_data
        self.db = DatabaseManager()
        
        # Create admin interface
        self.create_widgets()
        
        # Load initial data
        self.load_trips()
        self.load_all_bookings()
    
    def create_widgets(self):
        """Create admin interface widgets"""
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.parent_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Trip Management Tab
        self.trip_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.trip_frame, text="Trip Management")
        self.create_trip_management()
        
        # Booking Management Tab
        self.booking_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.booking_frame, text="All Bookings")
        self.create_booking_management()
        
        # Statistics Tab
        self.stats_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.stats_frame, text="Statistics")
        self.create_statistics()
    
    def create_trip_management(self):
        """Create trip management interface"""
        # Add trip section
        add_frame = ttk.LabelFrame(self.trip_frame, text="Add New Trip", padding="15")
        add_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Form fields
        form_frame = ttk.Frame(add_frame)
        form_frame.pack(fill=tk.X)
        
        # Row 1
        row1 = ttk.Frame(form_frame)
        row1.pack(fill=tk.X, pady=5)
        
        ttk.Label(row1, text="Source:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.source_var = tk.StringVar()
        source_combo = ttk.Combobox(row1, textvariable=self.source_var, width=15)
        source_combo['values'] = ('Delhi', 'Mumbai', 'Bangalore', 'Chennai', 'Kolkata', 'Hyderabad', 'Pune', 'Ahmedabad')
        source_combo.grid(row=0, column=1, padx=(0, 20))
        
        ttk.Label(row1, text="Destination:").grid(row=0, column=2, sticky=tk.W, padx=(0, 5))
        self.destination_var = tk.StringVar()
        dest_combo = ttk.Combobox(row1, textvariable=self.destination_var, width=15)
        dest_combo['values'] = ('Delhi', 'Mumbai', 'Bangalore', 'Chennai', 'Kolkata', 'Hyderabad', 'Pune', 'Ahmedabad')
        dest_combo.grid(row=0, column=3, padx=(0, 20))
        
        ttk.Label(row1, text="Date:").grid(row=0, column=4, sticky=tk.W, padx=(0, 5))
        self.date_var = tk.StringVar()
        ttk.Entry(row1, textvariable=self.date_var, width=12).grid(row=0, column=5)
        
        # Row 2
        row2 = ttk.Frame(form_frame)
        row2.pack(fill=tk.X, pady=5)
        
        ttk.Label(row2, text="Mode:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.mode_var = tk.StringVar()
        mode_combo = ttk.Combobox(row2, textvariable=self.mode_var, width=15)
        mode_combo['values'] = ('flight', 'train', 'bus')
        mode_combo.grid(row=0, column=1, padx=(0, 20))
        
        ttk.Label(row2, text="Price (₹):").grid(row=0, column=2, sticky=tk.W, padx=(0, 5))
        self.price_var = tk.StringVar()
        ttk.Entry(row2, textvariable=self.price_var, width=15).grid(row=0, column=3, padx=(0, 20))
        
        ttk.Label(row2, text="Seats:").grid(row=0, column=4, sticky=tk.W, padx=(0, 5))
        self.seats_var = tk.StringVar()
        ttk.Entry(row2, textvariable=self.seats_var, width=12).grid(row=0, column=5)
        
        # Row 3
        row3 = ttk.Frame(form_frame)
        row3.pack(fill=tk.X, pady=5)
        
        ttk.Label(row3, text="Departure:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.departure_var = tk.StringVar()
        ttk.Entry(row3, textvariable=self.departure_var, width=15).grid(row=0, column=1, padx=(0, 20))
        
        ttk.Label(row3, text="Arrival:").grid(row=0, column=2, sticky=tk.W, padx=(0, 5))
        self.arrival_var = tk.StringVar()
        ttk.Entry(row3, textvariable=self.arrival_var, width=15).grid(row=0, column=3, padx=(0, 20))
        
        ttk.Label(row3, text="Duration:").grid(row=0, column=4, sticky=tk.W, padx=(0, 5))
        self.duration_var = tk.StringVar()
        ttk.Entry(row3, textvariable=self.duration_var, width=12).grid(row=0, column=5)
        
        # Add button
        add_button = ttk.Button(add_frame, text="Add Trip", command=self.add_trip)
        add_button.pack(pady=(10, 0))
        
        # Trip list section
        list_frame = ttk.LabelFrame(self.trip_frame, text="Existing Trips", padding="15")
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create treeview for trips
        columns = ('ID', 'Source', 'Destination', 'Date', 'Mode', 'Price', 'Departure', 'Arrival', 'Duration', 'Seats')
        self.trips_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=10)
        
        # Define column headings and widths
        column_widths = {'ID': 50, 'Source': 100, 'Destination': 100, 'Date': 100, 
                        'Mode': 80, 'Price': 80, 'Departure': 80, 'Arrival': 80, 
                        'Duration': 80, 'Seats': 60}
        
        for col in columns:
            self.trips_tree.heading(col, text=col)
            self.trips_tree.column(col, width=column_widths[col])
        
        # Scrollbars
        v_scrollbar1 = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.trips_tree.yview)
        h_scrollbar1 = ttk.Scrollbar(list_frame, orient=tk.HORIZONTAL, command=self.trips_tree.xview)
        self.trips_tree.configure(yscrollcommand=v_scrollbar1.set, xscrollcommand=h_scrollbar1.set)
        
        # Grid treeview and scrollbars
        self.trips_tree.grid(row=0, column=0, sticky='nsew')
        v_scrollbar1.grid(row=0, column=1, sticky='ns')
        h_scrollbar1.grid(row=1, column=0, sticky='ew')
        
        list_frame.grid_rowconfigure(0, weight=1)
        list_frame.grid_columnconfigure(0, weight=1)
        
        # Trip action buttons
        trip_actions = ttk.Frame(list_frame)
        trip_actions.grid(row=2, column=0, columnspan=2, pady=10, sticky='ew')
        
        ttk.Button(trip_actions, text="Refresh", command=self.load_trips).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(trip_actions, text="Delete Selected", command=self.delete_trip).pack(side=tk.LEFT)
    
    def create_booking_management(self):
        """Create booking management interface"""
        # Bookings list
        bookings_frame = ttk.LabelFrame(self.booking_frame, text="All Bookings", padding="15")
        bookings_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create treeview for bookings
        columns = ('Booking ID', 'User', 'Email', 'Route', 'Date', 'Mode', 'Passengers', 'Amount', 'Status', 'Booked On')
        self.bookings_tree = ttk.Treeview(bookings_frame, columns=columns, show='headings', height=15)
        
        # Define column headings and widths
        column_widths = {
            'Booking ID': 80,
            'User': 120,
            'Email': 150,
            'Route': 150,
            'Date': 100,
            'Mode': 80,
            'Passengers': 80,
            'Amount': 100,
            'Status': 80,
            'Booked On': 120
        }
        
        for col in columns:
            self.bookings_tree.heading(col, text=col)
            self.bookings_tree.column(col, width=column_widths[col])
        
        # Scrollbars
        v_scrollbar2 = ttk.Scrollbar(bookings_frame, orient=tk.VERTICAL, command=self.bookings_tree.yview)
        h_scrollbar2 = ttk.Scrollbar(bookings_frame, orient=tk.HORIZONTAL, command=self.bookings_tree.xview)
        self.bookings_tree.configure(yscrollcommand=v_scrollbar2.set, xscrollcommand=h_scrollbar2.set)
        
        # Grid treeview and scrollbars
        self.bookings_tree.grid(row=0, column=0, sticky='nsew')
        v_scrollbar2.grid(row=0, column=1, sticky='ns')
        h_scrollbar2.grid(row=1, column=0, sticky='ew')
        
        bookings_frame.grid_rowconfigure(0, weight=1)
        bookings_frame.grid_columnconfigure(0, weight=1)
        
        # Booking action buttons
        booking_actions = ttk.Frame(bookings_frame)
        booking_actions.grid(row=2, column=0, columnspan=2, pady=10, sticky='ew')
        
        ttk.Button(booking_actions, text="Refresh", command=self.load_all_bookings).pack(side=tk.LEFT)
    
    def create_statistics(self):
        """Create statistics interface"""
        stats_main = ttk.Frame(self.stats_frame)
        stats_main.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = ttk.Label(stats_main, text="Travel Booking Statistics", font=('Arial', 18, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # Statistics cards
        cards_frame = ttk.Frame(stats_main)
        cards_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Create statistics labels
        self.total_bookings_label = ttk.Label(cards_frame, text="Total Bookings: 0", font=('Arial', 12, 'bold'))
        self.total_bookings_label.pack(fill=tk.X, pady=5)
        
        self.total_revenue_label = ttk.Label(cards_frame, text="Total Revenue: ₹0", font=('Arial', 12, 'bold'))
        self.total_revenue_label.pack(fill=tk.X, pady=5)
        
        self.total_passengers_label = ttk.Label(cards_frame, text="Total Passengers: 0", font=('Arial', 12, 'bold'))
        self.total_passengers_label.pack(fill=tk.X, pady=5)
        
        self.popular_route_label = ttk.Label(cards_frame, text="Popular Route: N/A", font=('Arial', 12, 'bold'))
        self.popular_route_label.pack(fill=tk.X, pady=5)
        
        self.popular_mode_label = ttk.Label(cards_frame, text="Popular Mode: N/A", font=('Arial', 12, 'bold'))
        self.popular_mode_label.pack(fill=tk.X, pady=5)
        
        # Refresh button
        refresh_stats_button = ttk.Button(stats_main, text="Refresh Statistics", command=self.update_statistics)
        refresh_stats_button.pack(pady=20)
        
        # Load initial statistics
        self.update_statistics()
    
    def add_trip(self):
        """Add a new trip"""
        # Validate inputs
        if not all([self.source_var.get(), self.destination_var.get(), self.date_var.get(),
                   self.mode_var.get(), self.price_var.get(), self.seats_var.get(),
                   self.departure_var.get(), self.arrival_var.get(), self.duration_var.get()]):
            messagebox.showerror("Error", "Please fill in all fields")
            return
        
        try:
            # Validate date
            datetime.strptime(self.date_var.get(), '%Y-%m-%d')
            
            # Validate numeric fields
            price = float(self.price_var.get())
            seats = int(self.seats_var.get())
            
            if price <= 0 or seats <= 0:
                raise ValueError("Price and seats must be positive")
            
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {str(e)}")
            return
        
        # Add trip to database
        success, message = self.db.add_trip(
            self.source_var.get(),
            self.destination_var.get(),
            self.date_var.get(),
            price,
            self.mode_var.get(),
            self.duration_var.get(),
            self.departure_var.get(),
            self.arrival_var.get(),
            seats
        )
        
        if success:
            messagebox.showinfo("Success", "Trip added successfully!")
            # Clear form
            for var in [self.source_var, self.destination_var, self.date_var, self.mode_var,
                       self.price_var, self.seats_var, self.departure_var, self.arrival_var, self.duration_var]:
                var.set('')
            self.load_trips()
        else:
            messagebox.showerror("Error", message)
    
    def load_trips(self):
        """Load all trips"""
        trips = self.db.search_trips()
        
        # Clear existing items
        for item in self.trips_tree.get_children():
            self.trips_tree.delete(item)
        
        # Insert trip data
        for trip in trips:
            trip_id, source, destination, date, price, mode, duration, departure, arrival, seats, created_at = trip
            
            self.trips_tree.insert('', tk.END, values=(
                trip_id, source, destination, date, mode.title(), 
                f"₹{price:,.0f}", departure, arrival, duration, seats
            ))
    
    def delete_trip(self):
        """Delete selected trip"""
        selection = self.trips_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a trip to delete.")
            return
        
        # Get selected trip data
        item = self.trips_tree.item(selection[0])
        trip_id = item['values'][0]
        
        # Confirm deletion
        confirmation = messagebox.askyesno(
            "Confirm Deletion",
            f"Are you sure you want to delete trip #{trip_id}?\n\n"
            f"This action cannot be undone."
        )
        
        if confirmation:
            success, message = self.db.delete_trip(trip_id)
            if success:
                messagebox.showinfo("Success", "Trip deleted successfully!")
                self.load_trips()
            else:
                messagebox.showerror("Error", message)
    
    def load_all_bookings(self):
        """Load all bookings"""
        bookings = self.db.get_all_bookings()
        
        # Clear existing items
        for item in self.bookings_tree.get_children():
            self.bookings_tree.delete(item)
        
        # Insert booking data
        for booking in bookings:
            booking_id, user_name, email, passengers, total_amount, booking_date, status, source, destination, date, mode = booking
            
            # Format data
            route = f"{source} → {destination}"
            amount_str = f"₹{total_amount:,.0f}"
            
            # Format booking date
            booking_dt = datetime.fromisoformat(booking_date.replace('Z', '+00:00'))
            booked_on = booking_dt.strftime('%Y-%m-%d %H:%M')
            
            # Color code by status
            tags = ()
            if status == 'confirmed':
                tags = ('confirmed',)
            elif status == 'cancelled':
                tags = ('cancelled',)
            elif status == 'pending':
                tags = ('pending',)
            
            self.bookings_tree.insert('', tk.END, values=(
                booking_id, user_name, email, route, date, mode.title(), 
                passengers, amount_str, status.title(), booked_on
            ), tags=tags)
        
        # Configure tag colors
        self.bookings_tree.tag_configure('confirmed', background='#dcfce7')
        self.bookings_tree.tag_configure('cancelled', background='#fecaca')
        self.bookings_tree.tag_configure('pending', background='#fef3c7')
    
    def update_statistics(self):
        """Update statistics display"""
        bookings = self.db.get_all_bookings()
        
        # Calculate statistics
        total_bookings = len(bookings)
        confirmed_bookings = [b for b in bookings if b[6] == 'confirmed']
        total_revenue = sum([b[4] for b in confirmed_bookings])
        total_passengers = sum([b[3] for b in confirmed_bookings])
        
        # Popular route
        if confirmed_bookings:
            routes = [f"{b[7]} → {b[8]}" for b in confirmed_bookings]
            popular_route = max(set(routes), key=routes.count) if routes else "N/A"
            
            # Popular mode
            modes = [b[10] for b in confirmed_bookings]
            popular_mode = max(set(modes), key=modes.count).title() if modes else "N/A"
        else:
            popular_route = "N/A"
            popular_mode = "N/A"
        
        # Update labels
        self.total_bookings_label.configure(text=f"Total Bookings: {total_bookings}")
        self.total_revenue_label.configure(text=f"Total Revenue: ₹{total_revenue:,.0f}")
        self.total_passengers_label.configure(text=f"Total Passengers: {total_passengers}")
        self.popular_route_label.configure(text=f"Popular Route: {popular_route}")
        self.popular_mode_label.configure(text=f"Popular Mode: {popular_mode}")