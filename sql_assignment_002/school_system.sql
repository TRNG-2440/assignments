CREATE TABLE Principals(
	principal_id INT PRIMARY KEY,
	name VARCHAR(100),
	hire_date DATE,
	salary DECIMAL(10,2)
);

CREATE TABLE Schools (
	school_id INT PRIMARY KEY,
	name VARCHAR(100),
	principal_id INT,
	FOREIGN KEY (principal_id) REFERENCES Principals(principal_id)
);

CREATE TABLE Students(
	student_id INT PRIMARY KEY,
	name VARCHAR(100),
	grade VARCHAR(10),
	home_address VARCHAR(255), 
	emergency_contact_number VARCHAR(20),
	school_id  INT,
	FOREIGN KEY (school_id) REFERENCES Schools(school_id)
	
);


