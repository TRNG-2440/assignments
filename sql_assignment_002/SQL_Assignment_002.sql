CREATE TABLE principal (
    full_name VARCHAR(100) PRIMARY KEY,
    hire_date DATE,
    salary DECIMAL(10, 2)
)

CREATE TABLE school(
    full_name VARCHAR(100) PRIMARY KEY,
    principal_full_name VARCHAR(100) References principal(full_name)
)

CREATE TABLE student(
    full_name VARCHAR(100) PRIMARY KEY,
    grade_level VARCHAR(10),
    home_addrs VARCHAR(200),
    emergency_contact_number VARCHAR(20),
    school_full_name VARCHAR(100) References school(full_name)
)