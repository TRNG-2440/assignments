--Mark White
--2026-06-26
--Assignment#9

SELECT d.first_name, d.last_name
FROM hospital.doctor d
WHERE d.doctor_id NOT IN (
    SELECT doctor_id
    FROM hospital.appointment
);
