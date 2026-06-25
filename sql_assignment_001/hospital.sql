-- schema
DROP SCHEMA IF EXISTS hospital CASCADE;

CREATE SCHEMA hospital;

-- department
CREATE TABLE hospital.department (
    department_id SERIAL PRIMARY KEY,
    department_name VARCHAR(50),
    location VARCHAR(50)
);

-- doctor
CREATE TABLE hospital.doctor (
    doctor_id SERIAL PRIMARY KEY,
    department_id INTEGER REFERENCES hospital.department,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    specialty VARCHAR(50),
    phone VARCHAR(20)
);

-- patient
CREATE TABLE hospital.patient (
    patient_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    date_of_birth DATE,
    phone VARCHAR(20),
    address VARCHAR(50)
);

-- appointment
CREATE TABLE hospital.appointment (
    appointment_id SERIAL PRIMARY KEY,
    patient_id INTEGER REFERENCES hospital.patient,
    doctor_id INTEGER REFERENCES hospital.doctor,
    appointment_date DATE NOT NULL,
    appointment_time TIME NOT NULL,
    reason VARCHAR(100),
    status VARCHAR(50)
);

-- prescription
CREATE TABLE hospital.prescription (
    prescription_id SERIAL PRIMARY KEY,
    appointment_id INTEGER REFERENCES hospital.appointment,
    medication_name VARCHAR(50),
    dosage VARCHAR(20),
    instructions VARCHAR(150)
);

-- room
CREATE TABLE hospital.room (
    room_id SERIAL PRIMARY KEY,
    department_id INTEGER REFERENCES hospital.department,
    room_number VARCHAR(20),
    room_type VARCHAR(30),
    is_available BOOLEAN
);