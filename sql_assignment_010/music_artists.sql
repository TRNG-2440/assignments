drop schema if exists music cascade;

create schema music;

create table music.genres(
    genre_id int primary key,
    genre_name varchar(200)
);

create table music.bands(
    band_id int primary key,
    genre_id int references music.genres(genre_id),
    band_name varchar(300)
);

create table music.musicians(
    musician_id int primary key,
    band_id int references music.bands(band_id),
    musician_name varchar(300),
    instrument varchar(200)
);


insert into music.genres(genre_id, genre_name)
values
    (1, 'Rock'),
    (2, 'Jazz'),
    (3, 'Pop'),
    (4, 'Folk');

insert into music.bands(band_id, genre_id, band_name)
values
    (1, 1, 'The Midnight Echo'),
    (2, 2, 'Blue Ember Quartet'),
    (3, 3, 'Neon Parade'),
    (4, 1, 'Hollow Crown'),
    (5, 4, 'Cedar & Pine');

insert into music.musicians(musician_id, band_id, musician_name, instrument)
values
    (1, 1, 'Dana Reeves', 'Guitar'),
    (2, 1, 'Leo Marsh', 'Drums'),
    (3, 2, 'Priya Anand', 'Saxophone'),
    (4, 2, 'Sam Okafor', 'Piano'),
    (5, 3, 'Cleo Vance', 'Vocals'),
    (6, 4, 'Jordan Hale', 'Bass'),
    (7, 5, 'Mia Sorrel', 'Acoustic Guitar'),
    (8, 5, 'Finn Calloway', 'Violin');



-- musician, band they play, and genre
select musician_name, band_name as band, genre_name as genre
from music.musicians m
join music.bands b on m.band_id = b.band_id
join music.genres g on m.genre_id = b.genre_id;