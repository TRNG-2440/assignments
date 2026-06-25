SELECT
    m.musician_name,
    b.band_name,
    g.genre_name
FROM Music.Musician m
INNER JOIN Music.Band b ON m.band_id = b.band_id
INNER JOIN Music.Genre g ON b.genre_id = g.genre_id
ORDER BY g.genre_name, b.band_name, m.musician_name;

SELECT
    m.musician_name,
    m.instrument,
    b.band_name
FROM Music.Musician m
INNER JOIN Music.Band b ON m.band_id = b.band_id
INNER JOIN Music.Genre g ON b.genre_id = g.genre_id
WHERE g.genre_name = 'Rock'
ORDER BY b.band_name, m.musician_name;