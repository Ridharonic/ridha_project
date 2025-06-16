import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# Import our modules
from login import LoginWindow
from search import SearchWindow
from booking import BookingWindow
from admin import AdminPanel
from db import DatabaseManager

class TravelBookingApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("TravelBook - Travel Booking System")
        self.root.geometry("1200x700")
        self.root.minsize(1000, 600)
        
        # Initialize database
        self.db = DatabaseManager()
        
        # User data
        self.current_user = None
        
        # Configure styles
        self.setup_styles()
        
        # Center window
        self.center_window()
        
        # Start with login
        self.show_login()
    
    def center_window(self):
        """Center the main window on screen"""
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (1200 // 2)
        y = (self.root.winfo_screenheight() // 2) - (700 // 2)
        self.root.geometry(f"1200x700+{x}+{y}")
    
    def setup_styles(self):
        """Setup application styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure custom styles
        style.configure('Header.TLabel', font=('Arial', 16, 'bold'), foreground='#1f2937')
        style.configure('Title.TLabel', font=('Arial', 20, 'bold'), foreground='#2563eb')
        style.configure('Nav.TButton', font=('Arial', 11))
        
        # Configure notebook style
        style.configure('TNotebook.Tab', padding=[20, 10])
    
    def show_login(self):
        """Show login window"""
        # Clear main window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Create login window
        self.login_window = LoginWindow(self.root, self.on_login_success)
    
    def on_login_success(self, user_data):
        """Handle successful login"""
        self.current_user = user_data
        self.show_main_application()
    
    def show_main_application(self):
        """Show main application interface"""
        # Clear window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Create main layout
        self.create_main_layout()
    
    def create_main_layout(self):
        """Create main application layout"""
        # Header
        header_frame = ttk.Frame(self.root)
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Title and user info
        title_frame = ttk.Frame(header_frame)
        title_frame.pack(side=tk.LEFT)
        
        title_label = ttk.Label(title_frame, text="TravelBook", style='Title.TLabel')
        title_label.pack(side=tk.LEFT)
        
        user_frame = ttk.Frame(header_frame)
        user_frame.pack(side=tk.RIGHT)
        
        user_label = ttk.Label(user_frame, text=f"Welcome, {self.current_user['name']}", font=('Arial', 12))
        user_label.pack(side=tk.LEFT, padx=(0, 20))
        
        if self.current_user['is_admin']:
            admin_badge = ttk.Label(user_frame, text="ADMIN", font=('Arial', 10, 'bold'), 
                                   foreground='white', background='#dc2626')
            admin_badge.pack(side=tk.LEFT, padx=(0, 20))
        
        logout_button = ttk.Button(user_frame, text="Logout", command=self.logout)
        logout_button.pack(side=tk.LEFT)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Search Trips Tab
        self.search_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.search_frame, text="🔍 Search Trips")
        self.search_window = SearchWindow(self.search_frame, self.current_user, self.refresh_bookings)
        
        # My Bookings Tab
        self.booking_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.booking_frame, text="📅 My Bookings")
        self.booking_window = BookingWindow(self.booking_frame, self.current_user)
        
        # Admin Panel Tab (only for admins)
        if self.current_user['is_admin']:
            self.admin_frame = ttk.Frame(self.notebook)
            self.notebook.add(self.admin_frame, text="⚙️ Admin Panel")
            self.admin_window = AdminPanel(self.admin_frame, self.current_user)
        
        # Status bar
        self.status_bar = ttk.Label(self.root, text="Ready", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Bind window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def refresh_bookings(self):
        """Refresh bookings display"""
        if hasattr(self, 'booking_window'):
            self.booking_window.load_bookings()
    
    def logout(self):
        """Logout user"""
        confirmation = messagebox.askyesno("Confirm Logout", "Are you sure you want to logout?")
        if confirmation:
            self.current_user = None
            self.show_login()
    
    def on_closing(self):
        """Handle application closing"""
        if messagebox.askokcancel("Quit", "Do you want to quit the application?"):
            self.root.destroy()
    
    def run(self):
        """Start the application"""
        try:
            self.root.mainloop()
        except Exception as e:
            messagebox.showerror("Error", f"Application error: {str(e)}")
            sys.exit(1)

def main():
    """Main function"""
    # Check if running from correct directory
    if not os.path.exists('db.py'):
        messagebox.showerror("Error", "Please run this application from the correct directory.")
        sys.exit(1)
    
    # Create and run application
    app = TravelBookingApp()
    app.run()

if __name__ == "__main__":
    main()