SELECT p.player_id
FROM Player p 
JOIN Team t
    ON p.team_id = t.team_id
JOIN Sport s
    ON t.sport_id = s.sport_id
WHERE t.sport_id = 40001
AND p.player_salary > 200000;