--Mark White
--6/25/2026
--hospital schema



DROP SCHEMA IF EXISTS hospital CASCADE;
CREATE SCHEMA hospital;

CREATE TABLE hospital.departments (
    department_id serial PRIMARY KEY,
    department_name VARCHAR(50) NOT NULL,
    location VARCHAR(50) NOT NULL
);

CREATE TABLE hospital.doctors (
    doctor_id serial PRIMARY KEY,
    department_id INT NOT NULL, 
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    specialization VARCHAR(50) NOT NULL,
    phone VARCHAR(10) NOT NULL,

    CONSTRAINT fk_doctors_department 
        FOREIGN KEY (department_id) REFERENCES hospital.departments (department_id)
);

CREATE TABLE hospital.patients (
    patient_id serial PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    date_of_birth DATE NOT NULL,
    address VARCHAR(100) NOT NULL,
    phone VARCHAR(10) NOT NULL
);

CREATE TABLE hospital.appointments (
    appointment_id serial PRIMARY KEY,
    patient_id INT NOT NULL,
    doctor_id INT NOT NULL,
    appointment_date DATE NOT NULL,
    appointment_time TIME NOT NULL,
    reason VARCHAR(255) NOT NULL,
    status VARCHAR(50) NOT NULL,

    CONSTRAINT fk_appointments_patient 
        FOREIGN KEY (patient_id) REFERENCES hospital.patients (patient_id),

    CONSTRAINT fk_appointments_doctor 
        FOREIGN KEY (doctor_id) REFERENCES hospital.doctors (doctor_id)
);

CREATE TABLE hospital.prescriptions (
    prescription_id serial PRIMARY KEY,
    appointment_id INT NOT NULL,
    medication_name VARCHAR(50) NOT NULL,
    dosage VARCHAR(50) NOT NULL,
    instructions VARCHAR(255) NOT NULL,

    CONSTRAINT fk_prescriptions_appointment 
        FOREIGN KEY (appointment_id) REFERENCES hospital.appointments (appointment_id)
);

CREATE TABLE hospital.rooms (
    room_id serial PRIMARY KEY,
    department_id INT NOT NULL,
    room_number VARCHAR(10) NOT NULL,
    room_type VARCHAR(50) NOT NULL,
    is_available BOOLEAN NOT NULL,

    CONSTRAINT fk_rooms_department 
        FOREIGN KEY (department_id) REFERENCES hospital.departments (department_id)
);


