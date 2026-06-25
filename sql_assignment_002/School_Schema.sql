CREATE SCHEMA school;

CREATE TABLE school.principal(
	principal_id INT PRIMARY KEY,
	first_name VARCHAR,
	last_name VARCHAR,
	hire_date DATE,
	salary FLOAT
);

CREATE TABLE school.school(
	school_id INT PRIMARY KEY,
	principle_id INT REFERENCES school.principal(principal_id),
	school_name VARCHAR
);

CREATE TABLE school.student(
	student_id INT PRIMARY KEY,
	school_id INT REFERENCES school.school(school_id),
	first_name VARCHAR,
	last_name VARCHAR,
	grade INT,
	home_address VARCHAR,
	emergency_phone_number VARCHAR
);

