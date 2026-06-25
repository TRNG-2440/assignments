SELECT s.sport_name,
MAX(p.player_salary) AS highest_salary
FROM player p
JOIN team t ON p.team_id = t.team_id
JOIN sport s ON s.sport_id = t.sport_id
GROUP BY s.sport_name,p.player_salary
ORDER BY p.player_salary DESC
LIMIT 1;
