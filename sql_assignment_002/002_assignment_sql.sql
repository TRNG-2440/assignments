CREATE TABLE principal (
    principal_name VARCHAR(50) PRIMARY KEY,
    hire_date DATE,
    salary INT
);

CREATE TABLE school (
    school_name VARCHAR(50) PRIMARY KEY,
    principal_name VARCHAR(50),
    CONSTRAINT fk_school_principal
        FOREIGN KEY (principal_name)
        REFERENCES principal(principal_name)
);

CREATE TABLE student (
    student_name VARCHAR(50) PRIMARY KEY,
    student_grade VARCHAR(10),
    home_address VARCHAR(100),
    emergency_number VARCHAR(20),
    school_name VARCHAR(50),
    CONSTRAINT fk_student_school
        FOREIGN KEY (school_name)
        REFERENCES school(school_name)
);