--player jo
SELECT player_name AS player_jo
FROM player
WHERE
    LOWER(player_name) LIKE 'jo%';

-- player ae

SELECT player_name AS player_ae
FROM player
WHERE
    LOWER(player_name) LIKE '%a%e%';
