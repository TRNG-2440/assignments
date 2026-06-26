-- start with j followed by o
SELECT player_name
FROM player
WHERE LOWER(player_name) LIKE 'jo%'

-- contain an e some point after a 
SELECT player_name
FROM player
WHERE LOWER(player_name) LIKE '%a%e%'