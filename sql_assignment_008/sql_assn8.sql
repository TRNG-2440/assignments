-- j followed immediately by o

SELECT player_name
FROM Player
WHERE LOWER(player_name) LIKE 'jo%';

-- e at some point after a:

SELECT player_name
FROM Player
WHERE LOWER(player_name) LIKE '%a%e%';