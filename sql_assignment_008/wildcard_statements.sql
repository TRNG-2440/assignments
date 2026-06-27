--Mark White
--2026-06-26
--SQL ASSIGNMENT8



--Search for any name that starts with 'jo'
SELECT *
FROM sports.player p
WHERE p.player_name ILIKE 'jo%';

--Altered search for any name with an 'a' and an 'e'
SELECT *
FROM sports.player p
WHERE p.player_name ILIKE '%a%e%';
