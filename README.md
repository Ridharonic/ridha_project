# TravelBook - Travel Booking System

A Python desktop application for travel booking management built with tkinter.

## Requirements

- Python 3.6 or higher
- tkinter (usually comes pre-installed with Python)
- pillow (for image handling)

## Installation

1. Clone or download this project
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

To run the travel booking application:

```bash
python main.py
```

## Important Notes

- **tkinter**: This module is typically included with Python installations on Windows and macOS. On Linux systems, you may need to install it separately:
  - Ubuntu/Debian: `sudo apt-get install python3-tk`
  - CentOS/RHEL: `sudo yum install tkinter` or `sudo dnf install python3-tkinter`
  - Arch Linux: `sudo pacman -S tk`

- **WebContainer Limitation**: This application cannot run in browser-based environments like WebContainer as tkinter requires a desktop environment. Please run this application on your local machine.

## Features

- User authentication system
- Trip search and booking
- Booking management
- Admin panel for system administration
- SQLite database for data storage

## File Structure

- `main.py` - Main application entry point
- `login.py` - Login window implementation
- `search.py` - Trip search functionality
- `booking.py` - Booking management
- `admin.py` - Admin panel
- `db.py` - Database management
- `requirements.txt` - Python dependencies

## Usage

1. Run the application using `python main.py`
2. Login with your credentials or create a new account
3. Search for available trips
4. Make bookings and manage your reservations
5. Admin users can access the admin panel for system management