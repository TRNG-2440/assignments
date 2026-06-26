SELECT
    doc.first_name,
    doc.last_name,
    doc.doctor_id
FROM doctor AS doc
    LEFT JOIN appointment AS appt
        ON doc.doctor_id = appt.doctor_id
WHERE appt.doctor_id IS NULL
