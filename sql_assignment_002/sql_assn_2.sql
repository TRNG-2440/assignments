CREATE TABLE principal (
	principal_id INT PRIMARY KEY,
	principal_name VARCHAR(50),
	hire_date DATE,
	salary DECIMAL(10,2)
);

CREATE TABLE school (
	school_id INT PRIMARY KEY,
	principal_id INT REFERENCES principal(principal_id),
	school_name VARCHAR(50)
);

CREATE TABLE student (
	student_id INT PRIMARY KEY,
	school_id INT REFERENCES school(school_id),
	student_name VARCHAR(50),
	student_grade INT,
	home_address VARCHAR(100),
	emergency VARCHAR(50),
	contact_phone VARCHAR(11)
);