Create database if not exists `Hospital`;

use `Hospital`;

Set Foreign_Key_Checks = 0;

DROP TABLE IF EXISTS `Department`;
DROP TABLE IF EXISTS `Doctor`;
DROP TABLE IF EXISTS `Patient`;
DROP TABLE IF EXISTS `Appointment`;
DROP TABLE IF EXISTS `Prescription`;
DROP TABLE IF EXISTS `Room`;

CREATE TABLE Department 
(
    department_id int identity(1,1),
    department_name varchar(255) not null,
    location varchar(255) not null,

    Primary key(department_id)
);

CREATE Table Doctor
(
    doctor_id int identity(1,1),
    department_id int not null,
    first_name varchar(255) not null,
    last_name varchar(255) not null,
    specialty varchar(255) not null,

    Primary key(doctor_id),
    Foreign key(department_id) references Department(department_id)
);

Create Table Patient 
(
    patient_id int identity(1,1),
    first_name varchar(255) not null,
    last_name varchar(255) not null,
    date_of_birth date not null,
    gender varchar(255) not null,
    address varchar(255) not null,
    phone_number varchar(255) not null,

    Primary key(patient_id)
);

Create Table Appointment 
(
    appointment_id int identity(1,1),
    patient_id int not null,
    doctor_id int not null,
    appointment_date date not null,
    appointment_time time not null,
    reason varchar(255) not null
    status varchar(255) not null,

    Primary key(appointment_id),
    Foreign key(patient_id) references (Patient(patient_id)),
    Foreign key(doctor_id) references (Doctor(doctor_id))
);

Create Table Prescription
(
    prescription_id int identity(1,1),
    appointment_id int not null,
    medication_name varchar(255) not null,
    dosage varchar(255) not null,
    instructions varchar(255) not null,

    Primary key(prescription_id),
    Foreign key(appointment_id) references Appointment(appointment_id)
);

Create Table Room
(
    room_id int identity(1,1),
    department_id int not null,
    room_number varchar(255) not null,
    room_type varchar(255) not null,
    is_available boolean not null,

    Primary key (room_id),
    Foreign key(department_id) references Department(department_id)
);