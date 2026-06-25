-- assume db is for a school district (multiple schools)
-- schema
DROP SCHEMA IF EXISTS district CASCADE;

CREATE SCHEMA district;

-- principals
CREATE TABLE district.principals (
    principal_id SERIAL PRIMARY KEY,
    first_name VARCHAR(20),
    last_name VARCHAR(20),
    hire_date DATE NOT NULL,
    salary DECIMAL(10, 2)
);

-- schools
CREATE TABLE district.schools (
    school_id SERIAL PRIMARY KEY,
    name VARCHAR(50),
    principal_id INTEGER REFERENCES district.principals
);

-- students
CREATE TABLE district.students (
    student_id SERIAL PRIMARY KEY,
    first_name VARCHAR(20),
    last_name VARCHAR(20),
    grade VARCHAR(10),
    home_address VARCHAR(50),
    emergency_number VARCHAR(20),
    school_id INTEGER REFERENCES district.schools
);