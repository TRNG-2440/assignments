CREATE SCHEMA IF NOT EXISTS assignment_002;

DROP TABLE IF EXISTS assignment_002.principle CASCADE;
DROP TABLE IF EXISTS assignment_002.school CASCADE;
DROP TABLE IF EXISTS assignment_002.student CASCADE;

CREATE TABLE assignment_002.principle (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(32),
    last_name VARCHAR(32),
    salary INT
);

CREATE TABLE assignment_002.school (
    id SERIAL PRIMARY KEY,
    principle_id INT NOT NULL,
    school_name VARCHAR(64),
    CONSTRAINT principle_id_fk FOREIGN KEY (principle_id) REFERENCES assignment_002.principle(id)
);

CREATE TABLE assignment_002.student (
    id SERIAL PRIMARY KEY,
    school_id INT,
    first_name VARCHAR(32),
    last_name VARCHAR(32),
    grade VARCHAR(4),
    address VARCHAR(64),
    emergency_phone CHAR(10),
    CONSTRAINT school_id_fk FOREIGN KEY (school_id) REFERENCES assignment_002.school(id)
);