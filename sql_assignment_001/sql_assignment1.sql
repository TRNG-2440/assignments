-- clean up
DROP SCHEMA IF EXISTS hospital CASCADE;

--create schema
CREATE SCHEMA hospital;

--create tables -> decided on plural for table names

--department
--| location | varchar | --name location was not working so i changed it
CREATE TABLE hospital.departments (
    department_id INT PRIMARY KEY,
    department_name VARCHAR(100),
    department_location VARCHAR(100)
);

--doctor
CREATE TABLE hospital.doctors (
    doctor_id INT PRIMARY KEY,
    department_id INT REFERENCES hospital.departments (department_id),
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    specialty VARCHAR(100),
    phone VARCHAR(20)  -- +1 (###)-###-####

);

CREATE TABLE hospital.patients (
    patient_id INT PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    date_of_birth DATE,
    phone VARCHAR(100),
    address VARCHAR(100)
);

CREATE TABLE hospital.appointments (
    appointment_id INT PRIMARY KEY,
    patient_id INT REFERENCES hospital.patients (patient_id),
    doctor_id INT REFERENCES hospital.doctors (doctor_id),
    appointment_date DATE,
    appointment_time TIME,
    reason VARCHAR(100),
    appt_status VARCHAR(100)

);

CREATE TABLE hospital.prescriptions (
    prescription_id INT PRIMARY KEY,
    appointment_id INT REFERENCES hospital.appointments (appointment_id),
    medication_name VARCHAR(100),
    dosage VARCHAR(100),
    instructions VARCHAR(100)
);

CREATE TABLE hospital.rooms (
    room_id INT PRIMARY KEY,
    department_id INT REFERENCES hospital.departments (department_id),
    room_number VARCHAR(10),
    room_type VARCHAR(20),
    is_available BOOLEAN
);

-- insert data

--- test
