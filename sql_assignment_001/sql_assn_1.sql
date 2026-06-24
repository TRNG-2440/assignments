CREATE TABLE department (
	department_id INT PRIMARY KEY,
	department_name VARCHAR(50),
	department_location VARCHAR(50)
);

CREATE TABLE doctor (
	doctor_id INT PRIMARY KEY,
	department_id INT REFERENCES department(department_id),
	first_name VARCHAR(50),
	last_name VARCHAR(50),
	specialty VARCHAR(50),
	phone VARCHAR(11)
);

CREATE TABLE patient (
	patient_id INT PRIMARY KEY,
	first_name VARCHAR(50),
	last_name VARCHAR(50),
	date_of_birth DATE,
	phone VARCHAR(11),
	address VARCHAR(100)
);

CREATE TABLE appointment (
	appointment_id INT PRIMARY KEY,
	patient_id INT REFERENCES patient(patient_id),
	doctor_id INT REFERENCES doctor(doctor_id),
	appointment_date DATE,
	appointment_time TIME,
	reason VARCHAR(50),
	status VARCHAR(50)
);

CREATE TABLE prescription (
	prescription_id INT PRIMARY KEY,
	appointment_id INT REFERENCES appointment(appointment_id),
	medication_name VARCHAR(50),
	dosage VARCHAR(50),
	instructions VARCHAR(50)
);

CREATE TABLE room (
	room_id INT PRIMARY KEY,
	department_ID INT REFERENCES department(department_id),
	room_number VARCHAR(10),
	room_type VARCHAR(50),
	is_available BOOLEAN
);