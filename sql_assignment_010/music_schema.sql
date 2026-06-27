--Mark White
--2026-06-26
--Assignment#10

--music schema
DROP SCHEMA IF EXISTS music CASCADE;
CREATE SCHEMA music;

CREATE TABLE music.genre(
    genre_id SERIAL PRIMARY KEY,
    name VARCHAR(255)
);

CREATE TABLE music.band(
    band_id SERIAL PRIMARY KEY,
    band_name VARCHAR(255),
    genre_id INT, 

    CONSTRAINT fk_band_genre FOREIGN KEY (genre_id) REFERENCES music.genre(genre_id)
);

CREATE TABLE music.musician(
    musician_id SERIAL PRIMARY KEY,
    musician_name VARCHAR(255),
    band_id INT,
    instrument VARCHAR(255),

    CONSTRAINT fk_musician_band FOREIGN KEY (band_id) REFERENCES music.band(band_id)
);



-- insert data


--genre
INSERT INTO music.genre (genre_id, name) VALUES
(1, 'Rock'),
(2, 'Jazz'),
(3, 'Pop'),
(4, 'Folk');

--band
INSERT INTO music.band (band_id, genre_id, band_name) VALUES
(1, 1, 'The Midnight Echo'),
(2, 2, 'Blue Ember Quartet'),
(3, 3, 'Neon Parade'),
(4, 1, 'Hollow Crown'),
(5, 4, 'Cedar & Pine');

--musician
INSERT INTO music.musician (musician_id, band_id, musician_name, instrument) VALUES
(1, 1, 'Dana Reeves', 'Guitar'),
(2, 1, 'Leo Marsh', 'Drums'),
(3, 2, 'Priya Anand', 'Saxophone'),
(4, 2, 'Sam Okafor', 'Piano'),
(5, 3, 'Cleo Vance', 'Vocals'),
(6, 4, 'Jordan Hale', 'Bass'),
(7, 5, 'Mia Sorrel', 'Acoustic Guitar'),
(8, 5, 'Finn Calloway', 'Violin');
