CREATE TABLE IF NOT EXISTS Department(
    department_id SERIAL PRIMARY KEY,
    department_name VARCHAR(100),
    location VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS Room (
    room_id SERIAL PRIMARY KEY,
    department_id INTEGER,
    room_number VARCHAR(100),
    room_type VARCHAR(100),
    is_available BOOL,
    FOREIGN KEY(department_id) REFERENCES Department(department_id)
);

CREATE TABLE IF NOT EXISTS Doctor (
    doctor_id SERIAL PRIMARY KEY,
    department_id INTEGER,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    specialty VARCHAR(100),
    phone VARCHAR(20),
    FOREIGN KEY(department_id) REFERENCES Department(department_id)
);
 
CREATE TABLE IF NOT EXISTS Patient (
    patient_id SERIAL PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    date_of_birth DATE,
    phone VARCHAR(20),
    address VARCHAR(200)
);

CREATE TABLE IF NOT EXISTS Appointment(
    appointment_id SERIAL PRIMARY KEY,
    patient_id INTEGER,
    doctor_id INTEGER,
    appointment_date DATE,
    appointment_time TIME,
    reason TEXT,
    status VARCHAR(100),
    FOREIGN KEY(patient_id) REFERENCES Patient(patient_id),
    FOREIGN KEY(doctor_id) REFERENCES Doctor(doctor_id)
);

CREATE TABLE IF NOT EXISTS Prescription (
    prescription_id SERIAL PRIMARY KEY,
    appointment_id INTEGER,
    medication_name VARCHAR(100),
    dosage VARCHAR(100),
    instructions TEXT,
    FOREIGN KEY(appointment_id) REFERENCES Appointment(appointment_id)
);
