CREATE SCHEMA IF NOT EXISTS assignment_001
    AUTHORIZATION postgres;

DROP TABLE IF EXISTS assignment_001.appointment;
DROP TABLE IF EXISTS assignment_001.patient;
DROP TABLE IF EXISTS assignment_001.department;
DROP TABLE IF EXISTS assignment_001.doctor;
DROP TABLE IF EXISTS assignment_001.room;

CREATE TABLE assignment_001.department (
    department_id SERIAL PRIMARY KEY,
    department_name character varying(32),
    location character varying(64)
);

CREATE TABLE assignment_001.room
(
    room_id SERIAL PRIMARY KEY,
    department_id integer NOT NULL,
    room_number character(3),
    room_type character varying(16),
    is_available boolean DEFAULT true,
    CONSTRAINT department_id_fk FOREIGN KEY (department_id) REFERENCES assignment_001.department (department_id)
);

CREATE TABLE assignment_001.doctor (
    doctor_id SERIAL PRIMARY KEY,
    department_id integer NOT NULL,
    first_name VARCHAR(32),
    last_name VARCHAR(32),
    specialty VARCHAR(32),
    phone CHAR(10),
    CONSTRAINT department_id_fk FOREIGN KEY (department_id) REFERENCES assignment_001.department (department_id)
);

CREATE TABLE assignment_001.patient (
	patient_id SERIAL PRIMARY KEY,
	first_name VARCHAR(32),
	last_name VARCHAR(32),
	date_of_birth DATE,
	phone CHAR(10),
	address VARCHAR(64)
);

CREATE TABLE assignment_001.appointment (
    appointment_id SERIAL PRIMARY KEY,
    patient_id INT NOT NULL,
    doctor_id INT NOT NULL,
    appointment_date DATE,
    appointment_time TIME,
    reason VARCHAR(64),
    status VARCHAR(64),
    CONSTRAINT doctor_id_fk FOREIGN KEY (doctor_id) REFERENCES assignment_001.doctor (doctor_id)
);

CREATE TABLE assignment_001.prescription (
    prescription_id SERIAL PRIMARY KEY,
    appointment_id INT NOT NULL,
    medication_name VARCHAR(128),
    dosage VARCHAR(256),
    instructions VARCHAR(1028),
    CONSTRAINT appointment_id_fk FOREIGN KEY (appointment_id) REFERENCES assignment_001.appointment (appointment_id)
);