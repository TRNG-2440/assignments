CREATE TABLE IF NOT EXISTS genre(
    genre_id INTEGER PRIMARY KEY AUTOINCREMENT,
    genre_name TEXT
);

CREATE TABLE IF NOT EXISTS band(
    band_id INTEGER PRIMARY KEY AUTOINCREMENT,
    genre_id INTEGER,
    band_name TEXT,
    FOREIGN KEY (genre_id) REFERENCES genre(genre_id)
);

CREATE TABLE IF NOT EXISTS musician(
    musician_id INTEGER PRIMARY KEY AUTOINCREMENT,
    band_id INTEGER,
    musician_name TEXT,
    instrument text,
    FOREIGN KEY (band_id) REFERENCES band(band_id)
);

INSERT INTO genre(genre_name)
VALUES ('Rock'),
('Jazz'),
('Pop'),
('Folk');

INSERT INTO band(genre_id, band_name)
VALUES (1, 'The Midnight Echo'),
(2, 'Blue Ember Quartet'),
(3, 'Neon Parade'),
(1, 'Hollow Crown'),
(4, 'Cedar & Pine');

INSERT INTO musician(band_id, musician_name, instrument)
VALUES (1, 'Dana Reeves', 'Guitar'),
(1, 'Leo Marsh', 'Drums'),
(2, 'Priya Anand', 'Saxophone'),
(2, 'Sam Okafor', 'Piano'),
(3, 'Cleo Vance', 'Vocal'),
(4, 'Jordan Hale', 'Bass'),
(5, 'Mia Sorrel', 'Acoustic Guitar'),
(5, 'Finn Calloway', 'Violin');

SELECT m.musician_name, b.band_name, g.genre
FROM musician m 
JOIN band b 
ON m.band_id = b.band_id
JOIN genre g 
ON b.genre_id = g.genre_id;

SELECT m.musician_name, b.band_name, g.genre
FROM musician m 
JOIN band b
WHERE g.genre = 'Rock'
ON m.band_id = b.band_id
JOIN genre g 
ON b.genre_id = g.genre_id;
