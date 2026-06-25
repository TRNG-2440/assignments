SELECT Doctor.first_name, Doctor.last_name FROM Doctor
LEFT JOIN Appointment
    ON Doctor.doctor_id = Appointment.doctor_id
WHERE Appointment.status IS NULL
;

SELECT Doctor.first_name, Doctor.last_name FROM Doctor
LEFT JOIN Appointment
    ON Doctor.doctor_id = Appointment.doctor_id
WHERE Appointment.status IS NULL
OR Appointment.status <> 'Scheduled'
;
