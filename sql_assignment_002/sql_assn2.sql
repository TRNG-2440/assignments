CREATE TABLE Principal (
    principal_id INT PRIMARY KEY,
    name VARCHAR(50),
    hire_date DATE,
    salary DECIMAL(10, 2)
);

CREATE TABLE School (
    school_id INT PRIMARY KEY,
    name VARCHAR(50),
    principal_id INT,
    FOREIGN KEY (principal_id) REFERENCES Principal(principal_id)
);

CREATE TABLE Student (
    student_id INT PRIMARY KEY,
    name VARCHAR(50),
    grade VARCHAR(10),
    home_address VARCHAR(100),
    emergency_contact_phone VARCHAR(20),
    school_id INT,
    FOREIGN KEY (school_id) REFERENCES School(school_id)
);