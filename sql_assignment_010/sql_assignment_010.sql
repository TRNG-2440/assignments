-- Given the following tables, produce a result that shows each musician alongside the band they play in and what genre that band performs.

select Musician.musician_name, Band.band_name, Genre.genre_name from Musician
join Band on Musician.band_id = Band.band_id
join Genre on Band.genre_id = Genre.genre_id;

------------------------------------------------------------------------------------------------

-- **Stretch Goal:** Write a second query that returns only musicians who play in a Rock band. *Note: consider which table holds the genre name you want to filter on.*

select Musician.musician_name, Band.band_name, Genre.genre_name from Musician
join Band on Musician.band_id = Band.band_id
join Genre on Band.genre_id = Genre.genre_id
where Genre.genre_name = 'Rock';