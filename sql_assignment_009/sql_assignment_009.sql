select * from Doctor 
left join Appointment
on Doctor.doctor_id = Appointment.doctor_id
where Appointment.appointment_id is null;
