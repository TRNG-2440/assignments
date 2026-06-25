CREATE TABLE department (
    department_id INT PRIMARY KEY,
    department_name VARCHAR(100),
    location VARCHAR(100)
);

CREATE TABLE patient (
    patient_id INT PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    date_of_birth DATE,
    phone VARCHAR(100),
    address VARCHAR(100)
);

CREATE TABLE doctor (
    doctor_id INT PRIMARY KEY,
    department_id INT,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    specialty VARCHAR(100),
    phone VARCHAR(20),
    CONSTRAINT fk_doctor_department
        FOREIGN KEY (department_id)
        REFERENCES department(department_id)
);

CREATE TABLE room (
    room_id INT PRIMARY KEY,
    department_id INT,
    room_number VARCHAR(20),
    room_type VARCHAR(100),
    is_available BOOLEAN,
    CONSTRAINT fk_room_department
        FOREIGN KEY (department_id)
        REFERENCES department(department_id)
);

CREATE TABLE appointment (
    appointment_id INT PRIMARY KEY,
    patient_id INT,
    doctor_id INT,
    appointment_date DATE,
    appointment_time TIME,
    reason VARCHAR(255),
    status VARCHAR(50),
    CONSTRAINT fk_appointment_patient
        FOREIGN KEY (patient_id)
        REFERENCES patient(patient_id),
    CONSTRAINT fk_appointment_doctor
        FOREIGN KEY (doctor_id)
        REFERENCES doctor(doctor_id)
);

CREATE TABLE prescription (
    prescription_id INT PRIMARY KEY,
    appointment_id INT,
    medication_name VARCHAR(100),
    dosage VARCHAR(100),
    instructions VARCHAR(100),
    CONSTRAINT fk_prescription_appointment
        FOREIGN KEY (appointment_id)
        REFERENCES appointment(appointment_id)
);