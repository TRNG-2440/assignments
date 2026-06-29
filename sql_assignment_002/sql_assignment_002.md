# Exercise DDL given Description

Given the following information, create SQL scripts to create the three tables described.

Principles have a name, hire date, and salary.
Schools have a name, and a reference to a principle
Students have a name, a Grade (7th, 8th, 9th, etc...), a home address, an emergency contact phone number, and a reference to a school


THE FOLLOWING IS MY ANSWER
```sql
CREATE TABLE Principle
(
    principle_name VARCHAR(50) PRIMARY KEY,
    hire_date DATE,
    salary DECIMAL(10,2)
);

CREATE TABLE School
(
    school_name VARCHAR(50) PRIMARY KEY,
    principle_name VARCHAR(50) NOT NULL REFERENCES Principle(principle_name)
);

CREATE TABLE Student
(
    student_name VARCHAR(50) PRIMARY KEY,
    grade VARCHAR(16) NOT NULL,
    home_address VARCHAR(100) NOT NULL,
    emergency_contact_phone_number INT,
    school_name VARCHAR(50) NOT NULL REFERENCES School(student_name)
);
```