drop schema if exists hospital cascade;

create schema hospital;

create table hospital.department(
    department_id int primary key,
    department_name varchar(100),
    location varchar(200)
);


create table hospital.doctor(
    doctor_id int primary key,
    department_id int references hospital.department(department_id),
    first_name varchar(200),
    last_name varchar(200),
    specialty varchar(100),
    phone varchar(10)
);


create table hospital.patient(
    patient_id int primary key,
    first_name varchar(200),
    last_name varchar(200),
    date_of_birth date,
    phone varchar(10),
    patient_address varchar(500)
);


create table hospital.appointments(
    appointment_id int primary key,
    patient_id int references hospital.patient(patient_id),
    doctor_id int references hospital.doctor(doctor_id),
    appointment_date date,
    appointment_time timestamp,
    reason varchar(500),
    appointment_status varchar(50)
);


create table hospital.prescriptions(
    prescription_id int primary key,
    appointment_id int references hospital.appointments(appointment_id),
    medication_name varchar(200),
    dosage varchar(50),
    instructructions varchar(1000)
);


create table hospital.room(
    room_id int primary key,
    department_id int references hospital.department(department_id),
    room_number varchar(200),
    room_type varchar(100),
    is_available boolean
);