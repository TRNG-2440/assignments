--Mark White
--SQL Assignment 2
--2026-06-25
--Education Schema 


-- Principles have a name, hire date, and salary.
-- Schools have a name, and a reference to a principle
-- Students have a name, a Grade (7th, 8th, 9th, etc...), a home address, an emergency contact phone number, and a reference to a school


DROP SCHEMA IF EXISTS education CASCADE;
CREATE SCHEMA education;
CREATE TABLE education.principals (
    principal_id SERIAL PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    hire_date DATE NOT NULL,
    salary NUMERIC NOT NULL,
    
    CONSTRAINT positive_salary CHECK (salary > 0),
    CONSTRAINT valid_hire_date CHECK (hire_date <= CURRENT_DATE)
    
);

CREATE TABLE education.schools (
    id SERIAL PRIMARY KEY,
    principal_id INTEGER NOT NULL,
    name VARCHAR(255) NOT NULL,
    school_address VARCHAR(255),

    CONSTRAINT fk_school_principals FOREIGN KEY (principal_id) REFERENCES education.principals(principal_id)

);


CREATE TABLE education.students (
    student_id SERIAL PRIMARY KEY,
    school_id INTEGER NOT NULL REFERENCES education.schools(id),
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    grade INTEGER NOT NULL
        CHECK (grade BETWEEN 7 AND 12),
    home_address VARCHAR(255) NOT NULL,
    emergency_contact_phone_number VARCHAR(255) NOT NULL,

    CONSTRAINT fk_school_students FOREIGN KEY (school_id) REFERENCES education.schools(id)
);