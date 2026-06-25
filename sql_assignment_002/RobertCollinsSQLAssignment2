CREATE TABLE Principal (
    principal_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    hire_date DATE,
    salary DECIMAL(10, 2) 
);

CREATE TABLE School (
    school_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    principal_id INT,
    FOREIGN KEY (principal_id) REFERENCES Principal(principal_id)
);

CREATE TABLE Student (
    student_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    grade VARCHAR(10),
    home_address VARCHAR(200),
    emergency_contact_phone VARCHAR(20),
    school_id INT,
    FOREIGN KEY (school_id) REFERENCES School(school_id)
);