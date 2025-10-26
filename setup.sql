--Tested and verified by <avrahtac> on MySQL Workbench 8.0 CE (Microsoft Windows 11 72D29E7D-F4C6-427B-B4EE-FF314F8F9741)

CREATE DATABASE IF NOT EXISTS airline_db;


USE airline_db;

CREATE TABLE IF NOT EXISTS User (
    UserID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(255) NOT NULL,
    Email VARCHAR(255) NOT NULL UNIQUE,
    Phone VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS Flight (
    FlightID INT PRIMARY KEY AUTO_INCREMENT,
    FlightNumber VARCHAR(20) NOT NULL,
    Origin VARCHAR(100) NOT NULL,
    Destination VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS FlightSchedule (
    ScheduleID INT PRIMARY KEY AUTO_INCREMENT,
    FlightID INT NOT NULL,
    DepartureTime DATETIME NOT NULL,
    ArrivalTime DATETIME NOT NULL,
    PlaneModel VARCHAR(100) NOT NULL,
    TotalSeats INT NOT NULL,
    FOREIGN KEY (FlightID) REFERENCES Flight(FlightID) ON DELETE CASCADE
    -- (I added ON DELETE CASCADE, which is good practice)
);

CREATE TABLE IF NOT EXISTS Booking (
    BookingID INT PRIMARY KEY AUTO_INCREMENT,
    UserID INT NOT NULL,
    ScheduleID INT NOT NULL,
    PassengerName VARCHAR(255) NOT NULL, 
    Seat VARCHAR(10) NOT NULL,
    MealOption VARCHAR(50),
    Luggage VARCHAR(50),
    PaymentMethod VARCHAR(50),
    TotalPrice DECIMAL(10, 2) NOT NULL,
    BookingStatus VARCHAR(50) NOT NULL,
    BookingTime DATETIME NOT NULL,
    FOREIGN KEY (UserID) REFERENCES User(UserID),
    FOREIGN KEY (ScheduleID) REFERENCES FlightSchedule(ScheduleID)
);

SET FOREIGN_KEY_CHECKS = 0; -- Turn off checks to allow truncating
TRUNCATE TABLE User;
TRUNCATE TABLE Flight;
TRUNCATE TABLE FlightSchedule;
TRUNCATE TABLE Booking;
SET FOREIGN_KEY_CHECKS = 1; -- Turn checks back on

-- 5. Insert Sample Data 
INSERT INTO Flight(FlightNumber, Origin, Destination) VALUES ('AI-201', 'Mumbai', 'Delhi');
INSERT INTO Flight(FlightNumber, Origin, Destination) VALUES ('AI-202', 'Delhi', 'Mumbai');
INSERT INTO Flight(FlightNumber, Origin, Destination) VALUES ('6E-505', 'Pune', 'Bangalore');
-- (The IDs will be 1, 2, 3)

INSERT INTO FlightSchedule(FlightID, DepartureTime, ArrivalTime, PlaneModel, TotalSeats)
VALUES (1, '2025-10-28 08:00:00', '2025-10-28 10:00:00', 'Airbus A320', 180);

INSERT INTO FlightSchedule(FlightID, DepartureTime, ArrivalTime, PlaneModel, TotalSeats)
VALUES (2, '2025-10-28 11:00:00', '2025-10-28 13:00:00', 'Boeing 737', 180);

INSERT INTO FlightSchedule(FlightID, DepartureTime, ArrivalTime, PlaneModel, TotalSeats)
VALUES (3, '2025-10-28 14:00:00', '2025-10-28 15:30:00', 'Airbus A320', 180);


-- 6. Commit the changes
COMMIT;