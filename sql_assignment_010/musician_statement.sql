-- Mark White
-- 2026-06-26
-- Assignment#10

-- list musician name, band name, and genre

SELECT m.musician_name,
       b.band_name,
       g.name AS genre
FROM music.musician m
JOIN music.band b
    ON m.band_id = b.band_id
JOIN music.genre g
    ON b.genre_id = g.genre_id;
