SELECT first_name, last_name
FROM Doctor D
LEFT JOIN Appointment A ON A.doctor_id = D.doctor_id
WHERE appointment_id IS NULL;

SELECT D.first_name, D.last_name
FROM Doctor D
LEFT JOIN Appointment A ON A.doctor_id = D.doctor_id and A.status = 'Scheduled'
WHERE A.appointment_id IS NULL;