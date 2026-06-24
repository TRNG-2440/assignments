DROP TABLE IF EXISTS principles CASCADE;
CREATE TABLE IF NOT EXISTS principles (
    principle_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    hire_date DATE,
    salary DECIMAL
);

DROP TABLE IF EXISTS schools CASCADE;
CREATE TABLE IF NOT EXISTS schools (
    school_id SERIAL PRIMARY KEY,
    principle_id INTEGER,
    name VARCHAR(100),
    FOREIGN KEY(principle_id) REFERENCES principles(principle_id) ON DELETE CASCADE
);

DROP TABLE IF EXISTS students CASCADE;
CREATE TABLE IF NOT EXISTS students (
    student_id SERIAL PRIMARY KEY,
    school_id INTEGER,
    name VARCHAR(100),
    grade VARCHAR(3),
    address VARCHAR(200),
    emergency_contact_phone_number VARCHAR(20),
    FOREIGN KEY(school_id) REFERENCES schools(school_id) ON DELETE CASCADE
);
