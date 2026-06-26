SELECT p.player_name AS "Player Name", p.player_salary AS "Player Salary", s.sport_name
FROM sports.Player AS p
JOIN sports.Team AS t ON p.team_id = t.team_id
JOIN sports.Sport AS s ON t.sport_id = s.sport_id
ORDER BY p.player_salary DESC
LIMIT 1;