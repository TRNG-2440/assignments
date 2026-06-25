CREATE SCHEMA hospital;

CREATE TABLE hospital.department(
	department_id INTEGER PRIMARY KEY,
	department_name VARCHAR,
	location VARCHAR
);

CREATE TABLE hospital.room(
	room_id INTEGER PRIMARY KEY,
	department_id INTEGER REFERENCES hospital.department(department_id),
	room_number VARCHAR,
	room_type VARCHAR,
	is_available BOOLEAN
);

CREATE TABLE hospital.doctor(
	doctor_id INTEGER PRIMARY KEY,
	department_id INTEGER REFERENCES hospital.department(department_id),
	first_name VARCHAR,
	last_name VARCHAR,
	speciality VARCHAR,
	phone VARCHAR
);

CREATE TABLE hospital.patient(
	patient_id INTEGER PRIMARY KEY,
	first_name VARCHAR,
	last_name VARCHAR,
	date_of_birth VARCHAR,
	phone VARCHAR,
	address VARCHAR
);

CREATE TABLE hospital.appointment(
	appointment_id INTEGER PRIMARY KEY,
	patient_id INTEGER REFERENCES hospital.patient(patient_id),
	doctor_id INTEGER REFERENCES hospital.doctor(doctor_id),
	appointment_date DATE,
	appointment_time TIME,
	reason VARCHAR,
	status VARCHAR
);

CREATE TABLE hospital.prescription(
	prescription_id INTEGER PRIMARY KEY,
	appointment_id INTEGER REFERENCES hospital.appointment(appointment_id),
	medication_name VARCHAR,
	dosage VARCHAR,
	instructions VARCHAR
);