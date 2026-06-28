drop schema if exists hospital cascade;

create schema hospital;

create table hospital.departments(
    department_id int primary key,
    department_name varchar(200),
    department_location varchar(200)
);

create table hospital.doctors(
    doctor_id serial primary key,
    department_id int references hospital.departments(department_id),
    first_name varchar(500),
    last_name varchar(500),
    doctor_specialty varchar(500),
    doctor_phone varchar (10)
);


create table hospital.patients(
    patient_id serial primary key,
    patient_name varchar(500),
    patient_address varchar(1000),
    patient_phone varchar(10)
);

create table hospital.appointments(
    appointment_id serial primary key,
    patient_id int references hospital.patients(patient_id),
    doctor_id int references hospital.doctors(doctor_id),
    appointment_date date,
    appointment_time time,
    reason varchar(3000),
    appointment_status varchar(30)
);

insert into hospital.departments(department_id, department_name, department_location)
values
    (1, 'Cardiology', 'Building A'),
    (2, 'Neurology', 'Building B'),
    (3, 'Orthopedics', 'Building C'),
    (4, 'Pediatrics', 'Building D');

insert into hospital.doctors(doctor_id, department_id, first_name, last_name, doctor_specialty, doctor_phone)
values
    (1, 1, 'James', 'Mercer', 'Cardiologist', '555-1001'),
    (2, 1, 'Sandra', 'Yue', 'Cardiologist', '555-1002'),
    (3, 2, 'Omar', 'Haddad', 'Neurologist', '555-1003'),
    (4, 2, 'Priya', 'Nair', 'Neurologist', '555-1004'),
    (5, 3, 'Carlos', 'Reyes', 'Orthopedic Surgeon', '555-1005'),
    (6, 4, 'Beth', 'Olsen', 'Pediatrician', '555-1006'),
    (7, 4, 'Tom', 'Finch', 'Pediatrician', '555-1007');

insert into hospital.patients(patient_id, patient_name, patient_address, patient_phone)
values
    (1, 'Patient One', 'Address 1', '555-2001'),
    (2, 'Patient Two', 'Address 2', '555-2002'),
    (3, 'Patient Three', 'Address 3', '555-2003'),
    (4, 'Patient Four', 'Address 4', '555-2004'),
    (5, 'Patient Five', 'Address 5', '555-2005');

insert into hospital.appointments(appointment_id, patient_id, doctor_id, appointment_date, appointment_time, reason, appointment_status)
values
    (101, 1, 1, '2025-03-10', '09:00', 'Chest pain', 'Completed'),
    (102, 2, 3, '2025-03-11', '10:30', 'Migraines', 'Completed'),
    (103, 3, 1, '2025-03-12', '14:00', 'Follow-up', 'Scheduled'),
    (104, 4, 5, '2025-03-13', '11:00', 'Knee injury', 'Scheduled'),
    (105, 5, 2, '2025-03-14', '09:30', 'Annual check', 'Scheduled'),
    (106, 1, 4, '2025-03-15', '13:00', 'Headaches', 'Scheduled');



-- output all the doctors not in appointments table
select first_name as doctor_first_name, last_name as doctor_last_name
from hospital.doctors
where doctor_id not in (
    select doctor_id
    from hospital.appointments
    group by doctor_id
);