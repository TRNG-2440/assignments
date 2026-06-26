SELECT first_name, last_name FROM hospital.doctor doctor
	LEFT JOIN hospital.appointment appointment ON appointment.doctor_id = doctor.doctor_id
	WHERE appointment_id IS NULL;