-- allows for ties 
SELECT DISTINCT s.sport_name
FROM player p 
JOIN team t ON p.team_id = t.team_id
JOIN sport s ON t.sport_id = s.sport_id
WHERE s.player_salary = (
    SELECT MAX(player_salary)
    FROM player
)
