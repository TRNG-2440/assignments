CREATE SCHEMA Hospital;

CREATE TABLE Hospital.Department (
    department_id INT Primary Key,
    department_name VARCHAR(100),
    location VARCHAR(100)

);

CREATE TABLE Hospital.Doctor (
	doctor_id INT PRIMARY KEY,
    department_id INT,
	first_name VARCHAR(100),
	last_name VARCHAR(100),
	specialty VARCHAR(100),
    phone_number VARCHAR(20),
    FOREIGN KEY (department_id) REFERENCES Hospital.Department(department_id)
);

CREATE TABLE Hospital.Patient (
	patient_id INT PRIMARY KEY,
	first_name VARCHAR(100),
	last_name VARCHAR(100),
	date_of_birth DATE,
    phone_number VARCHAR(20),
    address VARCHAR(100)
);

CREATE TABLE Hospital.Appointment (
    appointment_id INT,
    patient_id INT,
    doctor_id INT,
    appointment_date DATE,
    appointment_time TIME,
    reason VARCHAR(100),
    status VARCHAR(100),
    FOREIGN KEY (patient_id) REFERENCES Hospital.Patient(patient_id),
    FOREIGN KEY (doctor_id) REFERENCES Hospital.Doctor(doctor_id)
);

CREATE TABLE Hospital.Prescription (
    prescription_id INT,
    appointment_id INT,
    medication_name VARCHAR(100),
    dosage VARCHAR(100),
    instructions VARCHAR(100),
    FOREIGN KEY (appointment_id) REFERENCES Hospital.Appointment(appointment_id)
);

CREATE TABLE Hospital.Room (
    room_id INT,
    department_id INT,
    room_number VARCHAR(100) NOT NULL,
    room_type VARCHAR(100),
    is_available BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (department_id) REFERENCES Hospital.Department(department_id)
);