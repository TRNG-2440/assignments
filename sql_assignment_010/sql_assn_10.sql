SELECT M.musician_name, B.band_name, G.genre_name
FROM Musician M
INNER JOIN Band B ON B.band_id = M.band_id
INNER JOIN Genre G ON G.genre_id = B.genre_id;

SELECT M.musician_name
FROM Musician M
INNER JOIN Band B ON B.band_id = M.band_id
INNER JOIN Genre G ON G.genre_id = B.genre_id
WHERE G.genre_name = 'Rock';