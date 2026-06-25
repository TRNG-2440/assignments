SELECT p.*
FROM Player p
JOIN Team t USING(team_id)
JOIN Sport s USING(sport_id)
WHERE s.sport_name = 'Foot Ball'
AND player_salary > 200000;