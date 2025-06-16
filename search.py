import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, date
from db import DatabaseManager

class SearchWindow:
    def __init__(self, parent_frame, user_data, on_book_trip):
        self.parent_frame = parent_frame
        self.user_data = user_data
        self.on_book_trip = on_book_trip
        self.db = DatabaseManager()
        
        # Create search interface
        self.create_widgets()
        
        # Load initial data
        self.load_trips()
    
    def create_widgets(self):
        """Create search interface widgets"""
        # Search form
        search_frame = ttk.LabelFrame(self.parent_frame, text="Search Trips", padding="15")
        search_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Search criteria
        criteria_frame = ttk.Frame(search_frame)
        criteria_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Source
        ttk.Label(criteria_frame, text="From:", font=('Arial', 10, 'bold')).grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.source_var = tk.StringVar()
        source_combo = ttk.Combobox(criteria_frame, textvariable=self.source_var, width=15)
        source_combo['values'] = ('', 'Delhi', 'Mumbai', 'Bangalore', 'Chennai', 'Kolkata', 'Hyderabad', 'Pune', 'Ahmedabad')
        source_combo.grid(row=0, column=1, padx=(0, 20))
        
        # Destination
        ttk.Label(criteria_frame, text="To:", font=('Arial', 10, 'bold')).grid(row=0, column=2, sticky=tk.W, padx=(0, 10))
        self.destination_var = tk.StringVar()
        destination_combo = ttk.Combobox(criteria_frame, textvariable=self.destination_var, width=15)
        destination_combo['values'] = ('', 'Delhi', 'Mumbai', 'Bangalore', 'Chennai', 'Kolkata', 'Hyderabad', 'Pune', 'Ahmedabad')
        destination_combo.grid(row=0, column=3, padx=(0, 20))
        
        # Date
        ttk.Label(criteria_frame, text="Date:", font=('Arial', 10, 'bold')).grid(row=1, column=0, sticky=tk.W, padx=(0, 10), pady=(10, 0))
        self.date_var = tk.StringVar()
        date_entry = ttk.Entry(criteria_frame, textvariable=self.date_var, width=18)
        date_entry.grid(row=1, column=1, padx=(0, 20), pady=(10, 0))
        
        # Date format hint
        ttk.Label(criteria_frame, text="(YYYY-MM-DD)", font=('Arial', 8), foreground='gray').grid(row=2, column=1, sticky=tk.W, pady=(2, 0))
        
        # Mode
        ttk.Label(criteria_frame, text="Mode:", font=('Arial', 10, 'bold')).grid(row=1, column=2, sticky=tk.W, padx=(0, 10), pady=(10, 0))
        self.mode_var = tk.StringVar()
        mode_combo = ttk.Combobox(criteria_frame, textvariable=self.mode_var, width=15)
        mode_combo['values'] = ('', 'flight', 'train', 'bus')
        mode_combo.grid(row=1, column=3, padx=(0, 20), pady=(10, 0))
        
        # Search buttons
        button_frame = ttk.Frame(search_frame)
        button_frame.pack(fill=tk.X)
        
        search_button = ttk.Button(button_frame, text="Search Trips", command=self.search_trips)
        search_button.pack(side=tk.LEFT, padx=(0, 10))
        
        clear_button = ttk.Button(button_frame, text="Clear", command=self.clear_search)
        clear_button.pack(side=tk.LEFT)
        
        show_all_button = ttk.Button(button_frame, text="Show All", command=self.load_trips)
        show_all_button.pack(side=tk.RIGHT)
        
        # Results frame
        results_frame = ttk.LabelFrame(self.parent_frame, text="Available Trips", padding="15")
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create treeview for trips
        columns = ('ID', 'Source', 'Destination', 'Date', 'Mode', 'Departure', 'Arrival', 'Duration', 'Price', 'Seats')
        self.trips_tree = ttk.Treeview(results_frame, columns=columns, show='headings', height=12)
        
        # Define column headings and widths
        column_widths = {'ID': 50, 'Source': 100, 'Destination': 100, 'Date': 100, 
                        'Mode': 80, 'Departure': 80, 'Arrival': 80, 'Duration': 80, 
                        'Price': 80, 'Seats': 60}
        
        for col in columns:
            self.trips_tree.heading(col, text=col)
            self.trips_tree.column(col, width=column_widths[col], minwidth=50)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.trips_tree.yview)
        h_scrollbar = ttk.Scrollbar(results_frame, orient=tk.HORIZONTAL, command=self.trips_tree.xview)
        self.trips_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack treeview and scrollbars
        self.trips_tree.grid(row=0, column=0, sticky='nsew')
        v_scrollbar.grid(row=0, column=1, sticky='ns')
        h_scrollbar.grid(row=1, column=0, sticky='ew')
        
        results_frame.grid_rowconfigure(0, weight=1)
        results_frame.grid_columnconfigure(0, weight=1)
        
        # Book button
        book_frame = ttk.Frame(self.parent_frame)
        book_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.book_button = ttk.Button(book_frame, text="Book Selected Trip", command=self.book_selected_trip)
        self.book_button.pack(side=tk.RIGHT)
        
        # Passengers selection
        ttk.Label(book_frame, text="Passengers:", font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=(0, 10))
        self.passengers_var = tk.IntVar(value=1)
        passengers_spin = ttk.Spinbox(book_frame, from_=1, to=10, textvariable=self.passengers_var, width=5)
        passengers_spin.pack(side=tk.LEFT, padx=(0, 20))
        
        # Bind double-click to book
        self.trips_tree.bind('<Double-1>', lambda e: self.book_selected_trip())
    
    def clear_search(self):
        """Clear search fields"""
        self.source_var.set('')
        self.destination_var.set('')
        self.date_var.set('')
        self.mode_var.set('')
    
    def search_trips(self):
        """Search trips based on criteria"""
        source = self.source_var.get().strip()
        destination = self.destination_var.get().strip()
        date_str = self.date_var.get().strip()
        mode = self.mode_var.get().strip()
        
        # Validate date format if provided
        if date_str:
            try:
                datetime.strptime(date_str, '%Y-%m-%d')
            except ValueError:
                messagebox.showerror("Error", "Invalid date format. Use YYYY-MM-DD")
                return
        
        # Search trips
        trips = self.db.search_trips(
            source=source if source else None,
            destination=destination if destination else None,
            date=date_str if date_str else None,
            mode=mode if mode else None
        )
        
        self.display_trips(trips)
        
        # Show search results count
        count = len(trips)
        if count == 0:
            messagebox.showinfo("Search Results", "No trips found matching your criteria.")
        else:
            messagebox.showinfo("Search Results", f"Found {count} trip(s) matching your criteria.")
    
    def load_trips(self):
        """Load all available trips"""
        trips = self.db.search_trips()
        self.display_trips(trips)
    
    def display_trips(self, trips):
        """Display trips in the treeview"""
        # Clear existing items
        for item in self.trips_tree.get_children():
            self.trips_tree.delete(item)
        
        # Insert trip data
        for trip in trips:
            trip_id, source, destination, date, price, mode, duration, departure, arrival, seats, created_at = trip
            
            # Format price
            price_str = f"₹{price:,.0f}"
            
            # Color code by mode
            tags = ()
            if mode == 'flight':
                tags = ('flight',)
            elif mode == 'train':
                tags = ('train',)
            elif mode == 'bus':
                tags = ('bus',)
            
            self.trips_tree.insert('', tk.END, values=(
                trip_id, source, destination, date, mode.title(), 
                departure, arrival, duration, price_str, seats
            ), tags=tags)
        
        # Configure tag colors
        self.trips_tree.tag_configure('flight', background='#dbeafe')
        self.trips_tree.tag_configure('train', background='#dcfce7')
        self.trips_tree.tag_configure('bus', background='#fed7aa')
    
    def book_selected_trip(self):
        """Book the selected trip"""
        selection = self.trips_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a trip to book.")
            return
        
        # Get selected trip data
        item = self.trips_tree.item(selection[0])
        trip_data = item['values']
        trip_id = trip_data[0]
        source = trip_data[1]
        destination = trip_data[2]
        date = trip_data[3]
        mode = trip_data[4]
        price_str = trip_data[8]
        available_seats = trip_data[9]
        
        passengers = self.passengers_var.get()
        
        if passengers > available_seats:
            messagebox.showerror("Error", f"Only {available_seats} seats available.")
            return
        
        # Extract price from formatted string
        price = float(price_str.replace('₹', '').replace(',', ''))
        total_amount = price * passengers
        
        # Confirm booking
        confirmation = messagebox.askyesno(
            "Confirm Booking",
            f"Booking Details:\n\n"
            f"Trip: {source} → {destination}\n"
            f"Date: {date}\n"
            f"Mode: {mode}\n"
            f"Passengers: {passengers}\n"
            f"Total Amount: ₹{total_amount:,.0f}\n\n"
            f"Confirm this booking?"
        )
        
        if confirmation:
            success, message = self.db.book_trip(self.user_data['user_id'], trip_id, passengers)
            if success:
                messagebox.showinfo("Success", "Trip booked successfully!")
                self.load_trips()  # Refresh the list
                if self.on_book_trip:
                    self.on_book_trip()  # Callback to parent
            else:
                messagebox.showerror("Booking Failed", message)