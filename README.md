# Airline Booking System

This project is a desktop application for a database management course, simulating a flight booking system. It features a separate frontend built with Python (Tkinter) and a relational database backend powered by MySQL.

## Project Overview

The application provides a comprehensive booking experience. Users can book new flights by selecting a route, filling in passenger details, and choosing from available seats on a 180-passenger aircraft. The system includes crucial business logic, such as preventing the double-booking of a seat on a specific flight. It also allows users to customize their journey with in-flight meal and luggage preferences. A key component is the "My Dashboard" feature, which serves as a booking retrieval tool. By entering a unique Booking ID (PNR), the system queries the database and displays a complete, formatted "Boarding Pass" style itinerary, demonstrating the relational model by joining data from the `Booking`, `Flight`, `FlightSchedule`, and `User` tables.

## Technology Stack

* **Frontend:** Python 3, Tkinter
* **Backend:** MySQL Server
* **Connector:** `mysql-connector-python`

## Installation and Setup

To run this project, you will need Python 3 and a running MySQL server.

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/atharvachitale765/dbms_project.git](https://github.com/atharvachitale765/dbms_project.git)
    cd your-repo-name
    ```

2.  **Setup the Backend Database:**
    * Open MySQL Workbench (or any MySQL client).
    * Connect to your MySQL server.
    * Open and execute the `setup.sql` file. This will:
        1.  Create the `airline_db` database.
        2.  Create all required tables (`User`, `Flight`, `FlightSchedule`, `Booking`).
        3.  Insert sample flight data to populate the application.

3.  **Install Frontend Dependencies:**
    * This project requires the official MySQL connector for Python.
    ```bash
    pip install mysql-connector-python
    ```

4.  **Configure the Application:**
    * Open the `app.py` file in your code editor.
    * Locate the `DB_CONFIG` dictionary at the top of the file.
    * Update the `host`, `user`, and `password` values to match your MySQL server credentials.

## Running the Application

Once the database is set up and the application is configured, run the main file from your terminal:

```bash
python app.py