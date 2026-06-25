SELECT
    d.first_name,
    d.last_name
FROM Hospital.Doctor d
LEFT JOIN Hospital.Appointment a ON d.doctor_id = a.doctor_id
WHERE a.appointment_id IS NULL
ORDER BY d.last_name, d.first_name;