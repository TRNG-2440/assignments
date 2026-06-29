------------- DDL setup -------------

set foreign_key_checks = 0;

drop database if exists Library;

create database Library;

use Library;

set foreign_key_checks = 1;

------------- Schema ----------------

Create table if not exists Genre 
(
genre_id int identity(1,1),
genre_name varchar(255) not null unique

primary_key (genre_id)
);

---------------------------------------------------------

Create table if not exists Book 
(
  book_id int identity(1,1),
  title varchar(255) not null,
  author varchar(255) not null, 
  publication_year varchar(255) not null, 
  genre_id int not null,
  total_copy_count int not null default 1,

  primary_key(book_id),
  foreign key (genre_id) references Genre(genre_id)
);

---------------------------------------------------------

Create table if not exists member
(
  member_id int identity(1,1),
  full_name varchar(255) not null,
  email varchar(255) not null,
  join_date date not null
) ;

---------------------------------------------------------