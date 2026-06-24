CREATE TABLE Department (
    department_id   INT             PRIMARY KEY,
    department_name VARCHAR(255)    NOT NULL,
    location        VARCHAR(255)    NOT NULL
);

CREATE TABLE Room (
    room_id         INT             PRIMARY KEY,
    department_id   INT             NOT NULL,
    room_number     VARCHAR(64)     NOT NULL,
    room_type       VARCHAR(64)     NOT NULL,
    is_available    BOOL            NOT NULL,
    CONSTRAINT fk_department_id
    FOREIGN KEY (department_id)
    REFERENCES Department(department_id)
);

CREATE TABLE Doctor (
    doctor_id       INT             PRIMARY KEY,
    department_id   INT             NOT NULL,
    first_name      VARCHAR(255)    NOT NULL,
    last_name       VARCHAR(255)    NOT NULL,
    speciality      VARCHAR(255)    NOT NULL,
    phone           VARCHAR(15)     NOT NULL,
    CONSTRAINT fk_department_id
    FOREIGN KEY (department_id)
    REFERENCES Department(department_id)
);

CREATE TABLE Patient (
    patient_id      INT             PRIMARY KEY,
    first_name      VARCHAR(255)    NOT NULL,
    last_name       VARCHAR(255)    NOT NULL,
    date_of_birth   DATE            NOT NULL,
    phone           VARCHAR(15)     NOT NULL,
    address         VARCHAR(255)    NOT NULL
);

CREATE TABLE Appointment (
    appointment_id  INT             PRIMARY KEY,
    patient_id      INT             NOT NULL,
    doctor_id       INT             NOT NULL,
    appointment_date    DATE        NOT NULL,
    appointment_time    DATE        NOT NULL,
    reason          VARCHAR(1023)   DEFAULT NULL,
    status          VARCHAR(63)     NOT NULL,
    CONSTRAINT fk_patient_id
    FOREIGN KEY (patient_id)
    REFERENCES Patient(patient_id),
    CONSTRAINT fk_doctor_id
    FOREIGN KEY (doctor_id)
    REFERENCES Doctor(doctor_id)
);

CREATE TABLE Prescription (
    prescription_id INT             PRIMARY KEY,
    appointment_id  INT             NOT NULL,
    medication_name VARCHAR(255)    NOT NULL,
    dosage          VARCHAR(1023)   NOT NULL,
    instructions    VARCHAR(1023)   NOT NULL,
    CONSTRAINT fk_appointment_id
    FOREIGN KEY (appointment_id)
    REFERENCES Appointment(appointment_id)
);
