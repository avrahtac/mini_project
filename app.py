import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector  # Import the MySQL connector
import datetime
import random

# =====================================================================
#  PART 1: DATABASE CONFIGURATION
# =====================================================================

# !! IMPORTANT !!
# Update this dictionary with your MySQL 'root' user and password.
# The database name must match the one you created in 'setup.sql'.
DB_CONFIG = {
    'host': '127.0.0.1',
    'user': 'root',  # Or your MySQL username
    'password': 'root', # <-- PUT YOUR MYSQL PASSWORD HERE
    'database': 'airline_db'
}

# =====================================================================
#  PART 2: THE TKINTER APPLICATION
# =====================================================================
class AirlineApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Airline Booking System (MySQL Edition)")
        self.geometry("900x700")

        self.notebook = ttk.Notebook(self)
        
        self.booking_tab = ttk.Frame(self.notebook, padding=10)
        self.dashboard_tab = ttk.Frame(self.notebook, padding=10)

        self.notebook.add(self.booking_tab, text='Book a Flight')
        self.notebook.add(self.dashboard_tab, text='My Dashboard')
        
        self.notebook.pack(fill="both", expand=True)

        self.create_booking_widgets()
        self.create_dashboard_widgets()
        
        self.load_flights()

    def create_booking_widgets(self):
        frame = self.booking_tab
        
        pax_frame = ttk.LabelFrame(frame, text="Passenger Details", padding=10)
        pax_frame.pack(fill="x", expand=True, pady=5)

        ttk.Label(pax_frame, text="Full Name:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.pax_name_entry = ttk.Entry(pax_frame, width=40)
        self.pax_name_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(pax_frame, text="Email:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.pax_email_entry = ttk.Entry(pax_frame, width=40)
        self.pax_email_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(pax_frame, text="Phone:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.pax_phone_entry = ttk.Entry(pax_frame, width=40)
        self.pax_phone_entry.grid(row=2, column=1, padx=5, pady=5)

        flight_frame = ttk.LabelFrame(frame, text="Flight & Seat Selection", padding=10)
        flight_frame.pack(fill="x", expand=True, pady=10)

        ttk.Label(flight_frame, text="Select Flight:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.flight_combo = ttk.Combobox(flight_frame, state="readonly", width=60)
        self.flight_combo.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(flight_frame, text="Select Seat:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.seat_combo = ttk.Combobox(flight_frame, state="readonly", width=15)
        self.seat_combo['values'] = self.generate_seats(180)
        self.seat_combo.current(0)
        self.seat_combo.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        options_frame = ttk.LabelFrame(frame, text="Options & Payment", padding=10)
        options_frame.pack(fill="x", expand=True, pady=10)
        
        ttk.Label(options_frame, text="Meal Option:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.meal_combo = ttk.Combobox(options_frame, state="readonly", values=["Veg", "Non-Veg", "No Meal"])
        self.meal_combo.current(2)
        self.meal_combo.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        ttk.Label(options_frame, text="Luggage (kg):").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.luggage_combo = ttk.Combobox(options_frame, values=["15 kg (Standard)", "20 kg (+Rs. 800)", "25 kg (+Rs. 1500)"])
        self.luggage_combo.current(0)
        self.luggage_combo.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(options_frame, text="Payment Method:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.payment_combo = ttk.Combobox(options_frame, state="readonly", values=["Credit Card", "Debit Card", "UPI / NetBanking"])
        self.payment_combo.current(0)
        self.payment_combo.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        self.book_button = ttk.Button(frame, text="Confirm & Book Ticket", command=self.on_book_flight)
        self.book_button.pack(pady=20, ipady=10, fill="x", expand=True)

    def create_dashboard_widgets(self):
        frame = self.dashboard_tab
        
        search_frame = ttk.LabelFrame(frame, text="Find My Booking", padding=10)
        search_frame.pack(fill="x", expand=True, pady=5)
        
        ttk.Label(search_frame, text="Enter Booking ID (PNR):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.search_id_entry = ttk.Entry(search_frame, width=15)
        self.search_id_entry.grid(row=0, column=1, padx=5, pady=5)
        
        self.search_button = ttk.Button(search_frame, text="Search", command=self.on_search_booking)
        self.search_button.grid(row=0, column=2, padx=10, pady=5)
        
        results_frame = ttk.LabelFrame(frame, text="Your Boarding Pass Details", padding=10)
        results_frame.pack(fill="both", expand=True, pady=10)
        
        self.dashboard_text = tk.Text(results_frame, height=20, width=80, font=("Courier", 12), state="disabled", bg="#f0f0f0")
        self.dashboard_text.pack(fill="both", expand=True)
        
    def generate_seats(self, total_seats):
        rows = total_seats // 6
        seats = []
        for i in range(1, rows + 1):
            for char in ['A', 'B', 'C', 'D', 'E', 'F']:
                seats.append(f"{i}{char}")
        return seats

    def load_flights(self):
        """Fetches flights from the MySQL DB to populate the dropdown."""
        try:
            # Connect to MySQL
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT s.ScheduleID, f.FlightNumber, f.Origin, f.Destination, s.DepartureTime
                FROM FlightSchedule s
                JOIN Flight f ON s.FlightID = f.FlightID
                ORDER BY s.DepartureTime
            """)
            self.flight_data = cursor.fetchall()
            
            cursor.close()
            conn.close()
            
            # Format for display (MySQL DATETIME object is handled automatically)
            display_list = [f"ID {s[0]}: {s[1]} ({s[2]} -> {s[3]}) at {s[4]}" for s in self.flight_data]
            self.flight_combo['values'] = display_list
            if display_list:
                self.flight_combo.current(0)
                
        except Exception as e:
            messagebox.showerror("Load Error", f"Could not load flights from MySQL: {e}")

    def on_book_flight(self):
        name = self.pax_name_entry.get()
        email = self.pax_email_entry.get()
        phone = self.pax_phone_entry.get()
        
        selected_flight_str = self.flight_combo.get()
        selected_seat = self.seat_combo.get()
        selected_meal = self.meal_combo.get()
        selected_luggage = self.luggage_combo.get()
        selected_payment = self.payment_combo.get()
        
        if not name or not email or not selected_flight_str:
            messagebox.showerror("Error", "Please fill in Name, Email, and select a Flight.")
            return

        try:
            schedule_id = int(selected_flight_str.split(':')[0].replace('ID', '').strip())
        except:
            messagebox.showerror("Error", "Invalid flight selected.")
            return
            
        conn = None # Initialize conn to None
        cursor = None # Initialize cursor to None
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            
            # Step A: Create or find the User
            cursor.execute("SELECT UserID FROM User WHERE Email = %s", (email,))
            user_row = cursor.fetchone()
            
            if user_row:
                user_id = user_row[0]
            else:
                cursor.execute("INSERT INTO User(Name, Email, Phone) VALUES (%s, %s, %s)", (name, email, phone))
                user_id = cursor.lastrowid
            
            # --- START OF FIX ---
            # Step B: Check if the seat is already taken ON THIS FLIGHT
            cursor.execute(
                "SELECT BookingID FROM Booking WHERE ScheduleID = %s AND Seat = %s", 
                (schedule_id, selected_seat)
            )
            existing_booking = cursor.fetchone()
            
            if existing_booking:
                # Seat is taken! Show error and stop.
                messagebox.showerror(
                    "Seat Taken", 
                    f"Sorry, seat {selected_seat} is already booked on this flight. Please select another seat."
                )
                conn.rollback() # Cancel any changes (like the new user)
                return # Stop the booking process
            # --- END OF FIX ---

            # Step C: Create the Booking (This code now only runs if the seat is free)
            booking_time = datetime.datetime.now()
            
            cursor.execute("""
                INSERT INTO Booking (
                    UserID, ScheduleID, PassengerName, Seat, MealOption, Luggage, 
                    PaymentMethod, TotalPrice, BookingStatus, BookingTime
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                user_id, schedule_id, name, selected_seat, selected_meal, selected_luggage,
                selected_payment, 5000.0, "Confirmed", booking_time # Dummy price
            ))
            
            booking_id = cursor.lastrowid
            
            conn.commit() # Commit the transaction
            
            messagebox.showinfo(
                "Booking Confirmed!", 
                f"Success!\nYour Booking ID (PNR) is: {booking_id}\n\n"
                f"Passenger: {name}\n"
                f"Seat: {selected_seat}"
            )
            
            self.pax_name_entry.delete(0, 'end')
            self.pax_email_entry.delete(0, 'end')
            self.pax_phone_entry.delete(0, 'end')

        except Exception as e:
            if conn:
                conn.rollback() # Rollback changes on error
            messagebox.showerror("Booking Error", f"An error occurred: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def on_search_booking(self):
        booking_id = self.search_id_entry.get()
        if not booking_id:
            return

        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            # dictionary=True makes cursor return results as dictionaries (easier to read)
            cursor = conn.cursor(dictionary=True) 
            
            # MySQL uses %s for parameters
            cursor.execute("""
                SELECT 
                    b.BookingID, b.BookingStatus, b.PassengerName, b.Seat, b.MealOption, b.Luggage,
                    f.FlightNumber, f.Origin, f.Destination,
                    s.DepartureTime, s.ArrivalTime, s.PlaneModel,
                    u.Email, u.Phone
                FROM Booking b
                JOIN FlightSchedule s ON b.ScheduleID = s.ScheduleID
                JOIN Flight f ON s.FlightID = f.FlightID
                JOIN User u ON b.UserID = u.UserID
                WHERE b.BookingID = %s
            """, (booking_id,))
            
            result = cursor.fetchone() # Get the one result
            
            cursor.close()
            conn.close()
            
            self.dashboard_text.config(state="normal")
            self.dashboard_text.delete('1.0', 'end')
            
            if result:
                # Using dictionary keys makes this much cleaner
                display_string = f"""
        --- BOARDING PASS / ITINERARY ---

        BOOKING ID (PNR):   {result['BookingID']}
        STATUS:             {result['BookingStatus']}

        PASSENGER:          {result['PassengerName']}
        SEAT:               {result['Seat']}

        FLIGHT:             {result['FlightNumber']} ({result['Origin']} -> {result['Destination']})
        DEPARTURE:          {result['DepartureTime']}
        ARRIVAL:            {result['ArrivalTime']}
        
        AIRCRAFT:           {result['PlaneModel']}
        MEAL:               {result['MealOption']}
        LUGGAGE:            {result['Luggage']}

        CONTACT:            {result['Email']} / {result['Phone']}
        
        ------------------------------------
        -- This is your boarding pass. --
        -- Please be at the gate 45 minutes before departure. --
        ------------------------------------
                """
                self.dashboard_text.insert('1.0', display_string)
            else:
                self.dashboard_text.insert('1.0', f"No booking found for ID: {booking_id}")
            
            self.dashboard_text.config(state="disabled")

        except Exception as e:
            messagebox.showerror("Search Error", f"An error occurred: {e}")

# =====================================================================
#  PART 3: RUN THE APPLICATION
# =====================================================================
if __name__ == "__main__":
    app = AirlineApp()
    app.mainloop()