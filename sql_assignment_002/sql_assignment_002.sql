set foreign_key_checks = 0;

drop database if exists `School_Database`;

create database `School`;

use `School_Database`;

set foreign_key_checks = 1;

----------------------------------------------------------------

create table Principal
(
    principal_name varchar(255) not null,
    hire_date date not null,
    salary decimal(10,2) not null check (salary > 0),
    primary key (principal_name)
);

----------------------------------------------------------------

create table School
(
    school_name varchar(255) not null,
    principal_name varchar(255) not null,

    primary key (school_name),
    foreign key (principal_name) references Principal(principal_name)
);

----------------------------------------------------------------

create table Students
(
    student_name varchar(255) not null,
    school_name varchar(255) not null,
    grade int not null check (grade >= 7 and grade <= 12),
    home_address varchar(255) not null,
    phone_number char(10) not null check,

    primary key (student_name),
    foreign key (school_name) references School(school_name)
);

----------------------------------------------------------------
