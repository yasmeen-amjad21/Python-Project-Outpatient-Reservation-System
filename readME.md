# Outpatient Reservation System  
**Terminal-Based Python Application**

## Project Overview
The Outpatient Reservation System is a **terminal-based Python application** designed to manage outpatient clinic appointments efficiently.  
The system supports two types of users:

- **Patients**: register, view appointments, and cancel reservations.
- **Administrators**: manage doctors, view schedules, and create data backups.

The application uses **text files** for persistent data storage and applies **input validation, conflict checking, logging, and backup mechanisms** to ensure reliability and data integrity.

---

## Objectives
- Implement a real-world reservation system using **Python**
- Apply **file handling** for persistent storage
- Enforce **data validation and business rules**
- Practice **modular programming** and clean code design
- Simulate **user roles and access control** in a terminal environment

---

## Features

###  Patient Features
- Register as a new patient (auto-generated Patient ID)
- View appointment history (confirmed & cancelled)
- Cancel existing appointments (status updated, not deleted)

###  Admin Features
- Add new doctors with working days and hours
- View detailed doctor schedules
- Create system backups of all data files

###  System Features
- Input validation for IDs, dates, and times
- Conflict detection to prevent double booking
- Appointment status management (Confirmed / Cancelled)
- Activity logging with timestamps
- File-based backup system

---

##  Project Structure
Outpatient_Reservation_System/
├── main.py # Main application file
├── doctors.txt # Doctors data file
├── patients.txt # Patients data file
├── appointments.txt # Appointments data file
├── system.log # System activity log
├── backups/ # Backup directory
└── README.md # Project documentation


