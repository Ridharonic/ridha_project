import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import font
from db import DatabaseManager
import re

class LoginWindow:
    def __init__(self, root, on_login_success):
        self.root = root
        self.on_login_success = on_login_success
        self.db = DatabaseManager()
        
        # Configure window
        self.root.title("TravelBook - Login")
        self.root.geometry("450x600")
        self.root.resizable(False, False)
        
        # Center window
        self.center_window()
        
        # Configure styles
        self.setup_styles()
        
        # Create UI
        self.create_widgets()
        
        # Set focus
        self.email_entry.focus()
    
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (450 // 2)
        y = (self.root.winfo_screenheight() // 2) - (600 // 2)
        self.root.geometry(f"450x600+{x}+{y}")
    
    def setup_styles(self):
        """Setup custom styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure styles
        style.configure('Title.TLabel', font=('Arial', 24, 'bold'), foreground='#2563eb')
        style.configure('Subtitle.TLabel', font=('Arial', 11), foreground='#6b7280')
        style.configure('Heading.TLabel', font=('Arial', 12, 'bold'), foreground='#374151')
        style.configure('Custom.TEntry', fieldbackground='white', borderwidth=1, relief='solid')
        style.configure('Login.TButton', font=('Arial', 11, 'bold'))
        style.configure('Link.TButton', font=('Arial', 10), foreground='#2563eb')
        
        # Configure button hover effects
        style.map('Login.TButton',
                 background=[('active', '#1d4ed8')])
        style.map('Link.TButton',
                 foreground=[('active', '#1e40af')])
    
    def create_widgets(self):
        """Create and arrange widgets"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="40")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 30))
        
        title_label = ttk.Label(header_frame, text="TravelBook", style='Title.TLabel')
        title_label.pack()
        
        subtitle_label = ttk.Label(header_frame, text="Sign in to continue your journey", style='Subtitle.TLabel')
        subtitle_label.pack(pady=(5, 0))
        
        # Form container
        form_frame = ttk.Frame(main_frame)
        form_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Mode toggle (Login/Register)
        mode_frame = ttk.Frame(form_frame)
        mode_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.is_login_mode = tk.BooleanVar(value=True)
        
        login_radio = ttk.Radiobutton(mode_frame, text="Sign In", variable=self.is_login_mode, 
                                     value=True, command=self.toggle_mode)
        login_radio.pack(side=tk.LEFT, padx=(0, 20))
        
        register_radio = ttk.Radiobutton(mode_frame, text="Create Account", variable=self.is_login_mode, 
                                        value=False, command=self.toggle_mode)
        register_radio.pack(side=tk.LEFT)
        
        # Name field (only for registration)
        self.name_frame = ttk.Frame(form_frame)
        ttk.Label(self.name_frame, text="Full Name", style='Heading.TLabel').pack(anchor=tk.W, pady=(0, 5))
        self.name_entry = ttk.Entry(self.name_frame, font=('Arial', 11), style='Custom.TEntry')
        self.name_entry.pack(fill=tk.X, ipady=8)
        
        # Email field
        email_frame = ttk.Frame(form_frame)
        email_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(email_frame, text="Email Address", style='Heading.TLabel').pack(anchor=tk.W, pady=(0, 5))
        self.email_entry = ttk.Entry(email_frame, font=('Arial', 11), style='Custom.TEntry')
        self.email_entry.pack(fill=tk.X, ipady=8)
        
        # Password field
        password_frame = ttk.Frame(form_frame)
        password_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(password_frame, text="Password", style='Heading.TLabel').pack(anchor=tk.W, pady=(0, 5))
        self.password_entry = ttk.Entry(password_frame, show="*", font=('Arial', 11), style='Custom.TEntry')
        self.password_entry.pack(fill=tk.X, ipady=8)
        
        # Submit button
        self.submit_button = ttk.Button(form_frame, text="Sign In", command=self.handle_submit, style='Login.TButton')
        self.submit_button.pack(fill=tk.X, ipady=10)
        
        # Demo credentials info
        demo_frame = ttk.Frame(main_frame)
        demo_frame.pack(fill=tk.X, pady=(20, 0))
        
        demo_label = ttk.Label(demo_frame, text="Demo Credentials:", font=('Arial', 10, 'bold'), foreground='#059669')
        demo_label.pack(anchor=tk.W)
        
        demo_info = ttk.Label(demo_frame, text="Admin: admin@travel.com / admin123\nUser: Create new account", 
                             font=('Arial', 9), foreground='#065f46')
        demo_info.pack(anchor=tk.W, pady=(5, 0))
        
        # Bind Enter key
        self.root.bind('<Return>', lambda e: self.handle_submit())
        
        # Initial mode setup
        self.toggle_mode()
    
    def toggle_mode(self):
        """Toggle between login and registration modes"""
        if self.is_login_mode.get():
            self.name_frame.pack_forget()
            self.submit_button.configure(text="Sign In")
        else:
            self.name_frame.pack(fill=tk.X, pady=(0, 15), before=self.email_entry.master)
            self.submit_button.configure(text="Create Account")
    
    def validate_email(self, email):
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def handle_submit(self):
        """Handle form submission"""
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not email or not password:
            messagebox.showerror("Error", "Please fill in all required fields")
            return
        
        if not self.validate_email(email):
            messagebox.showerror("Error", "Please enter a valid email address")
            return
        
        if self.is_login_mode.get():
            self.handle_login(email, password)
        else:
            name = self.name_entry.get().strip()
            if not name:
                messagebox.showerror("Error", "Please enter your full name")
                return
            self.handle_register(name, email, password)
    
    def handle_login(self, email, password):
        """Handle login process"""
        success, result = self.db.login_user(email, password)
        
        if success:
            messagebox.showinfo("Success", f"Welcome back, {result['name']}!")
            self.on_login_success(result)
        else:
            messagebox.showerror("Login Failed", result)
    
    def handle_register(self, name, email, password):
        """Handle registration process"""
        if len(password) < 6:
            messagebox.showerror("Error", "Password must be at least 6 characters long")
            return
        
        success, message = self.db.register_user(name, email, password)
        
        if success:
            messagebox.showinfo("Success", "Account created successfully! Please sign in.")
            self.is_login_mode.set(True)
            self.toggle_mode()
            self.name_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Registration Failed", message)