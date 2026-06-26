SELECT d.first_name, d.last_name
FROM Doctor AS d
LEFT JOIN Appointment AS a ON d.doctor_id = a.doctor_id
WHERE a.appointment_id IS NULL;