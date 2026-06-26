SELECT s.sport_name
FROM sport s
JOIN team t 
ON s.sport_id = t.sport_id 
JOIN player p  
ON t.team_id = p.team_id 
ORDER BY p.player_salary DESC 
LIMIT(1);