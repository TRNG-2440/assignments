-- shows each musician alongside the band they play in and what genre that band performs.
SELECT m.musician_name, b.band_name, g.genre_name
FROM Musician m 
JOIN Band b USING(band_id)
JOIN Genre g USING(genre_id);

-- musicians who play only in a Rock band
SELECT m.musician_name
FROM Musician m 
JOIN Band b USING(band_id)
JOIN Genre g USING(genre_id)
WHERE g.genre_name = 'Rock';