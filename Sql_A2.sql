CREATE TABLE Principle (
    principle_name INT PRIMARY KEY,
    hire_date DATE,
    salary INT
);

CREATE TABLE School (
    school_name INT PRIMARY KEY,
    principle_name INT, 
    FOREIGN KEY (principle_name) REFERENCES Principle(principle_name) 
);


CREATE TABLE Student (
    student_name INT PRIMARY KEY,
    grade INT,
    address VARCHAR(100),
    emergency_contact_num VARCHAR(20),
    school_name INT, 
    FOREIGN KEY (school_name) REFERENCES School(school_name) 
);