-- doctors with no appts
SELECT CONCAT(first_name, ' ', last_name)
FROM doctor
WHERE doctor_id NOT IN (SELECT doctor_id FROM appointment);

-- doctors with no scheduled appts.
SELECT CONCAT(first_name, ' ', last_name)
FROM doctor
WHERE doctor_id NOT IN (
    SELECT doctor_id 
    FROM appointment
    WHERE status != 'Scheduled');