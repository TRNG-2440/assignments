SELECT d.first_name, d.last_name
FROM 
    Doctor d
LEFT JOIN 
    Appointment a ON d.doctor_id = a.doctor_id
where 
    a.appointment_id IS NULL;