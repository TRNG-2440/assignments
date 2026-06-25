SELECT s.sport_name 'sport'
FROM sport s
JOIN team t ON t.sport_id = s.sport_id
JOIN player p ON p.team_id = t.team_id
WHERE player_salary = (SELECT MAX(player_salary) FROM player)