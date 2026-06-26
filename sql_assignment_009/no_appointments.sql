
SELECT d.first_name, d.last_name
FROM Doctors d
LEFT JOIN Appointments a
	ON d.doctor_id = a.doctor_id
WHERE a.appointment_id IS NULL;