import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from db import DatabaseManager

class BookingWindow:
    def __init__(self, parent_frame, user_data):
        self.parent_frame = parent_frame
        self.user_data = user_data
        self.db = DatabaseManager()
        
        # Create booking interface
        self.create_widgets()
        
        # Load user bookings
        self.load_bookings()
    
    def create_widgets(self):
        """Create booking interface widgets"""
        # Header
        header_frame = ttk.Frame(self.parent_frame)
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        
        title_label = ttk.Label(header_frame, text="My Bookings", font=('Arial', 16, 'bold'))
        title_label.pack(side=tk.LEFT)
        
        refresh_button = ttk.Button(header_frame, text="Refresh", command=self.load_bookings)
        refresh_button.pack(side=tk.RIGHT)
        
        # Bookings frame
        bookings_frame = ttk.LabelFrame(self.parent_frame, text="Booking History", padding="15")
        bookings_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create treeview for bookings
        columns = ('Booking ID', 'Route', 'Date', 'Mode', 'Time', 'Duration', 'Passengers', 'Amount', 'Status', 'Booked On')
        self.bookings_tree = ttk.Treeview(bookings_frame, columns=columns, show='headings', height=15)
        
        # Define column headings and widths
        column_widths = {
            'Booking ID': 80,
            'Route': 150,
            'Date': 100,
            'Mode': 80,
            'Time': 120,
            'Duration': 80,
            'Passengers': 80,
            'Amount': 100,
            'Status': 80,
            'Booked On': 120
        }
        
        for col in columns:
            self.bookings_tree.heading(col, text=col)
            self.bookings_tree.column(col, width=column_widths[col], minwidth=50)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(bookings_frame, orient=tk.VERTICAL, command=self.bookings_tree.yview)
        h_scrollbar = ttk.Scrollbar(bookings_frame, orient=tk.HORIZONTAL, command=self.bookings_tree.xview)
        self.bookings_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack treeview and scrollbars
        self.bookings_tree.grid(row=0, column=0, sticky='nsew')
        v_scrollbar.grid(row=0, column=1, sticky='ns')
        h_scrollbar.grid(row=1, column=0, sticky='ew')
        
        bookings_frame.grid_rowconfigure(0, weight=1)
        bookings_frame.grid_columnconfigure(0, weight=1)
        
        # Action buttons
        action_frame = ttk.Frame(self.parent_frame)
        action_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.cancel_button = ttk.Button(action_frame, text="Cancel Selected Booking", command=self.cancel_booking)
        self.cancel_button.pack(side=tk.RIGHT, padx=(10, 0))
        
        self.view_button = ttk.Button(action_frame, text="View Details", command=self.view_booking_details)
        self.view_button.pack(side=tk.RIGHT)
        
        # Statistics frame
        stats_frame = ttk.LabelFrame(self.parent_frame, text="Booking Statistics", padding="15")
        stats_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.stats_label = ttk.Label(stats_frame, text="Loading statistics...", font=('Arial', 10))
        self.stats_label.pack()
        
        # Bind double-click to view details
        self.bookings_tree.bind('<Double-1>', lambda e: self.view_booking_details())
    
    def load_bookings(self):
        """Load user bookings"""
        bookings = self.db.get_user_bookings(self.user_data['user_id'])
        self.display_bookings(bookings)
        self.update_statistics(bookings)
    
    def display_bookings(self, bookings):
        """Display bookings in the treeview"""
        # Clear existing items
        for item in self.bookings_tree.get_children():
            self.bookings_tree.delete(item)
        
        # Insert booking data
        for booking in bookings:
            booking_id, passengers, total_amount, booking_date, status, source, destination, date, mode, departure_time, arrival_time, duration = booking
            
            # Format data
            route = f"{source} → {destination}"
            time_range = f"{departure_time} - {arrival_time}"
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
                booking_id, route, date, mode.title(), time_range, 
                duration, passengers, amount_str, status.title(), booked_on
            ), tags=tags)
        
        # Configure tag colors
        self.bookings_tree.tag_configure('confirmed', background='#dcfce7')
        self.bookings_tree.tag_configure('cancelled', background='#fecaca')
        self.bookings_tree.tag_configure('pending', background='#fef3c7')
    
    def update_statistics(self, bookings):
        """Update booking statistics"""
        total_bookings = len(bookings)
        confirmed_bookings = len([b for b in bookings if b[4] == 'confirmed'])
        cancelled_bookings = len([b for b in bookings if b[4] == 'cancelled'])
        total_spent = sum([b[2] for b in bookings if b[4] == 'confirmed'])
        total_passengers = sum([b[1] for b in bookings if b[4] == 'confirmed'])
        
        stats_text = (
            f"Total Bookings: {total_bookings} | "
            f"Confirmed: {confirmed_bookings} | "
            f"Cancelled: {cancelled_bookings} | "
            f"Total Spent: ₹{total_spent:,.0f} | "
            f"Total Passengers: {total_passengers}"
        )
        
        self.stats_label.configure(text=stats_text)
    
    def view_booking_details(self):
        """View detailed booking information"""
        selection = self.bookings_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a booking to view details.")
            return
        
        # Get selected booking data
        item = self.bookings_tree.item(selection[0])
        booking_data = item['values']
        
        # Create details window
        details_window = tk.Toplevel(self.parent_frame)
        details_window.title("Booking Details")
        details_window.geometry("400x500")
        details_window.resizable(False, False)
        
        # Center the window
        details_window.transient(self.parent_frame.winfo_toplevel())
        details_window.grab_set()
        
        # Create details content
        details_frame = ttk.Frame(details_window, padding="20")
        details_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(details_frame, text="Booking Details", font=('Arial', 16, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # Details
        details = [
            ("Booking ID:", booking_data[0]),
            ("Route:", booking_data[1]),
            ("Travel Date:", booking_data[2]),
            ("Mode:", booking_data[3]),
            ("Time:", booking_data[4]),
            ("Duration:", booking_data[5]),
            ("Passengers:", booking_data[6]),
            ("Total Amount:", booking_data[7]),
            ("Status:", booking_data[8]),
            ("Booked On:", booking_data[9])
        ]
        
        for label, value in details:
            detail_frame = ttk.Frame(details_frame)
            detail_frame.pack(fill=tk.X, pady=5)
            
            ttk.Label(detail_frame, text=label, font=('Arial', 10, 'bold')).pack(side=tk.LEFT)
            ttk.Label(detail_frame, text=str(value), font=('Arial', 10)).pack(side=tk.RIGHT)
        
        # Close button
        close_button = ttk.Button(details_frame, text="Close", command=details_window.destroy)
        close_button.pack(pady=(20, 0))
    
    def cancel_booking(self):
        """Cancel selected booking"""
        selection = self.bookings_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a booking to cancel.")
            return
        
        # Get selected booking data
        item = self.bookings_tree.item(selection[0])
        booking_data = item['values']
        booking_id = booking_data[0]
        status = booking_data[8].lower()
        
        if status != 'confirmed':
            messagebox.showwarning("Cannot Cancel", "Only confirmed bookings can be cancelled.")
            return
        
        # Confirm cancellation
        confirmation = messagebox.askyesno(
            "Confirm Cancellation",
            f"Are you sure you want to cancel booking #{booking_id}?\n\n"
            f"Route: {booking_data[1]}\n"
            f"Date: {booking_data[2]}\n"
            f"Amount: {booking_data[7]}\n\n"
            f"This action cannot be undone."
        )
        
        if confirmation:
            success, message = self.db.cancel_booking(booking_id, self.user_data['user_id'])
            if success:
                messagebox.showinfo("Success", "Booking cancelled successfully!")
                self.load_bookings()  # Refresh the list
            else:
                messagebox.showerror("Cancellation Failed", message)