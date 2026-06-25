CREATE SCHEMA assignment01;

CREATE TABLE assignment01.department(
		department_id INTEGER PRIMARY KEY,
		department_name Varchar(200),
		department_location VarChar(200)
);

CREATE TABLE assignment01.doctor(
		doctor_id INTEGER PRIMARY KEY,
		department_id INTEGER,
		first_name VARCHAR(200),
		last_name VARCHAR(200),
		speciality VARCHAR(200),
		phone Varchar(200),
		CONSTRAINT department_id_fk FOREIGN KEY (department_id) REFERENCES assignment01.department(department_id)
);

CREATE TABLE assignment01.patient(
		patient_id INTEGER PRIMARY KEY,
		first_name Varchar(200),
		last_name Varchar(200),
		date_of_birth Varchar(200),
		phone Varchar(200),
		address Varchar(200)
);

CREATE TABLE assignment01.appointment(
		appointment_id INTEGER PRIMARY KEY,
		patient_id INTEGER,
		doctor_id INTEGER,
		appointment_date DATE,
		appointment_time TIME,
		reason VARCHAR (200),
		status VARCHAR (200),

		CONSTRAINT patient_id_fk FOREIGN KEY (patient_id) REFERENCES assignment01.patient(patient_id),
		CONSTRAINT doctor_id_fk FOREIGN KEY (doctor_id) REFERENCES assignment01.doctor(doctor_id)
);

CREATE TABLE assignment01.prescription(
		prescription_id INTEGER PRIMARY KEY,
		appointment_id INTEGER,
		medication_name VARCHAR(200),
		dosage VARCHAR(200),
		instructions VARCHAR(200),

		CONSTRAINT appointment_id_fk FOREIGN KEY (appointment_id) REFERENCES assignment01.appointment(appointment_id)
);

CREATE TABLE assignment01.room(
		room_id INTEGER PRIMARY KEY,
		department_id INTEGER,
		room_number VARCHAR(200), 
		room_type VARCHAR(200),
		is_available BOOLEAN,

		CONSTRAINT department_id_fk FOREIGN KEY (department_id) REFERENCES assignment01.department(department_id)
);