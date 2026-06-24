CREATE TABLE Principal(
    name VARCHAR(50) PRIMARY KEY,
    hire_date DATE,
    salary INT
);

CREATE TABLE School(
    name VARCHAR(50) PRIMARY KEY,
    FOREIGN KEY (name) REFERENCES Principal(name)
);

CREATE TABLE Student(
    name VARCHAR(50),
    grade INT,
    home_address VARCHAR(50),
    phone INT,
    FOREIGN KEY (name) REFERENCES School(name)
);