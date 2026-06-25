-- SQLite
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS department(
    department_id INTEGER PRIMARY KEY AUTOINCREMENT,
    department_name TEXT NOT NULL,
    location TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS doctor(
    doctor_id INTEGER PRIMARY KEY AUTOINCREMENT,
    department_id INTEGER,
    first_name TEXT,
    last_name TEXT,
    specialty TEXT,
    phone TEXT,
    FOREIGN KEY department_id REFERENCES department(department_id)
);

CREATE TABLE IF NOT EXISTS patient(
    patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT,
    last_name TEXT,
    date_of_birth DATE,
    phone TEXT,
    address TEXT

CREATE TABLE IF NOT EXISTS room(
    room_id INTEGER PRIMARY KEY AUTOINCREMENT,
    department_id INTEGER ,
    room_number TEXT,
    room_type TEXT,
    is_available INTEGER NOT NULL CHECK(is_available IN (0, 1)),
    FOREIGN KEY department_id REFERENCES department(department_id)
);

CREATE TABLE IF NOT EXISTS appointment(
    appointment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER,
    doctor_id INTEGER,
    appointment_date DATE,
    appointment_time TEXT, 
    REASON TEXT,
    STATUS TEXT,
    FOREIGN KEY patient_id REFERENCES patient(patient_id),
    FOREIGN KEY doctor_id REFERENCES doctor(doctor_id)
);

CREATE TABLE IF NOT EXISTS perscription(
    perscription_id INTEGER PRIMARY KEY AUTOINCREMENT,
    appointment_id,
    medication_name TEXT,
    dosage TEXT,
    instructions TEXT,
    FOREIGN KEY appointment_id REFERENCES appointment(appointment_id)
);