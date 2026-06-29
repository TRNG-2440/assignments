-- Note, this is written specifically in the SQL Server dialect
-- I ended up swapping to Postgres for all later assignments to align with what is being taught in our course

CREATE TABLE Department
(
    department_id INT IDENTITY(1,1) PRIMARY KEY,
    department_name VARCHAR(50) NOT NULL,
    location VARCHAR(100) NOT NULL
);

CREATE TABLE Doctor
(
    doctor_id INT IDENTITY(1,1) PRIMARY KEY,
    department_id INT NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    specialty VARCHAR(50),
    phone VARCHAR(8),

    CONSTRAINT FK_Doctor_Department
        FOREIGN KEY (department_id)
        REFERENCES Department(department_id)
);

CREATE TABLE Patient
(
    patient_id INT IDENTITY(1,1) PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    date_of_birth DATE NOT NULL,
    phone INT,
    address VARCHAR(150)
);

CREATE TABLE Appointment
(
    appointment_id INT IDENTITY(1,1) PRIMARY KEY,
    patient_id INT NOT NULL,
    doctor_id INT NOT NULL,
    appointment_date DATE NOT NULL,
    appointment_time TIME NOT NULL,
    reason VARCHAR(300),
    status VARCHAR(50),

    CONSTRAINT FK_Appointment_Patient
        FOREIGN KEY (patient_id)
        REFERENCES Patient(patient_id),

    CONSTRAINT FK_Appointment_Doctor
        FOREIGN KEY (doctor_id)
        REFERENCES Doctor(doctor_id)
);

CREATE TABLE Prescription
(
    prescription_id INT IDENTITY(1,1) PRIMARY KEY,
    appointment_id INT NOT NULL,
    medication_name VARCHAR(100) NOT NULL,
    dosage VARCHAR(100) NOT NULL,
    instructions VARCHAR(300),

    CONSTRAINT FK_Prescription_Appointment
        FOREIGN KEY (appointment_id)
        REFERENCES Appointment(appointment_id)
);

CREATE TABLE Room
(
    room_id INT IDENTITY(1,1) PRIMARY KEY,
    department_id INT NOT NULL,
    room_number VARCHAR(5) NOT NULL,
    room_type VARCHAR(50),
    is_available BIT NOT NULL,

    CONSTRAINT FK_Room_Department
        FOREIGN KEY (department_id)
        REFERENCES Department(department_id)
);