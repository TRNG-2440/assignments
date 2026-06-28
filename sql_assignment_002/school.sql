drop schema if exists school cascade;

create schema school;

create table school.principles(
    principle_id int primary key,
    principle_name varchar(500),
    hire_date date,
    principle_salary decimal
);


create table school.schools(
    school_id int primary key,
    school_name varchar(300),
    principle_id int references school.principles(principle_id)
);

create table school.students(
    student_id int primary key,
    student_name varchar(500),
    grade int,
    home_address varchar(500),
    emergency_contact_phone varchar(10),
    school_id int references school.schools(school_id)
);