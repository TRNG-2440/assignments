CREATE TABLE IF NOT EXISTS principle(
    principle_id INTEGER PRIMARY KEY AUTOINCREMENT,
    principle_name TEXT,
    hire_date DATE,
    salary INT
);

CREATE TABLE IF NOT EXISTS school(
    school_id INTEGER PRIMARY KEY AUTOINCREMENT,
    principle_id INTEGER,
    FOREIGN KEY (principle_id) REFERENCES principle(principle_id)
);

CREATE TABLE IF NOT EXISTS student(
    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
    grade INT,
    home_address TEXT,
    emergency_phone TEXT,
    school_id INTEGER,
    FOREIGN KEY (school_id) REFERENCES school(school_id)
);

