INSERT INTO department(department_id, department_name, location)
VALUES (1,'Cardiology','Building A'),
(2,'Neurology','Building B'),
(3,'Orthopedics','Building C'),
(4,'Pediatrics','Building D');

INSERT INTO doctor(doctor_id, department_id, first_name, last_name, specialty, phone)
VALUES (1,1,'James','Mercer','Cardiologist','555-1001'),
(2,1,'Sandra','Yue','Cardiologist','555-1002'),
(3,2,'Omar','Haddad','Neurologist','555-1003'),
(4,2,'Priya','Nair','Neurologist','555-1004'),
(5,3,'Carlos','Reyes','Orthopedic Surgeon','555-1005'),
(6,4,'Beth','Olsen','Pediatrician','555-1006'),
(7,4,'Tom','Finch','Pediatrician','555-1007');

INSERT into appointment(appointment_id, patient_id, doctor_id, appointment_date, appointment_time, reason, status)
VALUES (101,1,1,'2025-03-10','09:00','Chest pain','Completed'),
(102,2,3,'2025-03-11','10:30','Migraines','Completed'),
(103,3,1,'2025-03-12','14:00','Follow-up','Scheduled'),
(104,4,5,'2025-03-13','11:00','Knee injury','Scheduled'),
(105,5,2,'2025-03-14','09:30','Annual check','Scheduled'),
(106,1,4,'2025-03-15','13:00','Headaches','Scheduled');

SELECT first_name, last_name
FROM doctor
WHERE doctor_id IN (
SELECT d.doctor_id
FROM doctor d
EXCEPT
SELECT a.doctor_id
FROM appointment a
);

SELECT first_name, last_name
FROM doctor
WHERE doctor_id IN (
SELECT d.doctor_id
FROM doctor d
EXCEPT
SELECT a.doctor_id
FROM appointment a
WHERE a.status = 'Scheduled'
);