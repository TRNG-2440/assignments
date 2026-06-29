-- doctors with no appointments
SELECT Doctor.first_name, Doctor.last_name
FROM Doctor
WHERE NOT EXISTS (
    SELECT 1
    FROM Appointment
    WHERE Appointment.doctor_id = Doctor.doctor_id
);

-- doctors with no currently scheduled appointments
SELECT Doctor.first_name, Doctor.last_name
FROM Doctor
WHERE NOT EXISTS (
    SELECT 1
    FROM Appointment
    WHERE Appointment.doctor_id = Doctor.doctor_id
    AND Appointment.status = 'Scheduled'
);