SELECT
    m.musician_name,
    b.band_name,
    g.genre_name
FROM band AS b
    INNER JOIN musician AS m
        ON b.band_id = m.band_id
    INNER JOIN genre AS g
        ON b.genre_id = g.genre_id;
