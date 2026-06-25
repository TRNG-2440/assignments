-- The names of all doctors who have no appointments at all in the Appointment table.
SELECT CONCAT(d.first_name, ' ' ,d.last_name) as doctor_name
FROM Doctor d 
LEFT JOIN Appointment a USING(doctor_id)
WHERE a.doctor_id IS NULL;

-- The names of all doctors who have no **currently scheduled** appointments
SELECT CONCAT_WS(' ', d.first_name, d.last_name) AS doctor_name
FROM Doctor d 
WHERE d.doctor_id IN (
    SELECT d.doctor_id
    FROM Doctor d 
    LEFT JOIN Appointment a USING(doctor_id)
    GROUP BY doctor_id
    HAVING COUNT(CASE WHEN status = 'Scheduled' THEN 1 ELSE NULL END) = 0
);