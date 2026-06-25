--clean
DROP SCHEMA IF EXISTS school CASCADE;

--create schema
CREATE SCHEMA school;
--create table
CREATE TABLE school.principals (
    principal_id INT PRIMARY KEY,
    p_name VARCHAR(100),
    hire_date DATE,
    salary INT
);

CREATE TABLE school.schools (
    school_id INT PRIMARY KEY,
    s_name VARCHAR(100),
    principal_id INT REFERENCES school.principals (principal_id)
);

CREATE TABLE school.students (
    student_id SERIAL PRIMARY KEY,
    student_name VARCHAR(100),
    grade VARCHAR(10),
    home_address VARCHAR(100),
    emergency_contact_name VARCHAR(50),
    emergency_contact_number VARCHAR(20),
    school_id INT REFERENCES school.schools (school_id)
);
