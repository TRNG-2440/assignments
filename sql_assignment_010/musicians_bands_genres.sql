SELECT musician_name, band_name, genre_name FROM music.musician musician
	INNER JOIN music.band band ON band.band_id = musician.band_id
	INNER JOIN music.genre genre ON genre.genre_id = band.genre_id