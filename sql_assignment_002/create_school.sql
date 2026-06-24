CREATE TABLE Principle (
    principle_id    INT             PRIMARY KEY,
    first_name      VARCHAR(255)    NOT NULL,
    last_name       VARCHAR(255)    NOT NULL,
    hire_date       DATE            NOT NULL,
    salary          DECIMAL(12, 2)  NOT NULL
);

CREATE TABLE School (
    school_id       INT             PRIMARY KEY,
    name            VARCHAR(255)    NOT NULL,
    principle_id    INT             NOT NULL,
    CONSTRAINT fk_principle_id
    FOREIGN KEY (principle_id)
    REFERENCES Principle(principle_id)
);

CREATE TABLE Student (
    student_id      INT             PRIMARY KEY,
    school_id       INT             NOT NULL,
    first_name      VARCHAR(255)    NOT NULL,
    last_name       VARCHAR(255)    NOT NULL,
    grade           VARCHAR(63)     NOT NULL,
    home_address    VARCHAR(1023)   NOT NULL,
    emergency_phone_contact VARCHAR(15) NOT NULL,
    CONSTRAINT fk_school_id
    FOREIGN KEY (school_id)
    REFERENCES School(school_id)
);
