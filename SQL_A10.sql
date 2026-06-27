SELECT 
    m.musician_name,
    b.band_name,
    g.genre_name
from 
    Musician m
INNER JOIN 
    Band b ON m.band_id = b.band_id
INNER JOIN 
    Genre g ON b.genre_id = g.genre_id;