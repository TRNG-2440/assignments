-- musicians with band and genre
SELECT m.musician_name, b.band_name, g.genre_name
FROM musician m
JOIN band b ON m.band_id = b.band_id
JOIN genre g ON b.genre_id = g.genre_id;

-- stretch goal, only rock band
SELECT m.musician_name, b.band_name, g.genre_name
FROM musician m
JOIN band b ON m.band_id = b.band_id
JOIN genre g ON b.genre_id = g.genre_id 
WHERE g.genre_name = 'Rock';