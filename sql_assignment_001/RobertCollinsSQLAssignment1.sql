CREATE SCHEMA Hospital;

CREATE TABLE Hospital.Department(
    department_id INTEGER Primary Key,

);


CREATE TABLE Hospital.Doctor(
		doctor_id INTEGER Primary Key,
        department_id INTEGER Foreign Key,
		first_name VARCHAR(200) NOT NULL,
		last_name VARCHAR(200) NOT NULL,
		specialty VARCHAR(100)
        phone_number VARCHAR(7)
);