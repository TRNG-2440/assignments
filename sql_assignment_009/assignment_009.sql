SELECT d.first_name, d.last_name FROM doctor d
WHERE d.doctor_id NOT IN (
	SELECT a.doctor_id
	FROM appointment a
	JOIN doctor d ON a.doctor_id = d.doctor_id
	GROUP BY a.doctor_id
	HAVING COUNT(a.doctor_id) > 0
);

SELECT d.first_name, d.last_name FROM doctor d
WHERE d.doctor_id NOT IN (
	SELECT a.doctor_id
	FROM appointment a
	JOIN doctor d ON a.doctor_id = d.doctor_id
    WHERE LOWER(a.status) != LOWER('Completed')
	GROUP BY a.doctor_id
	HAVING COUNT(a.doctor_id) > 0
);