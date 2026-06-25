SELECT 
    p.player_id,
    p.player_name,
    p.player_salary,
    t.team_name,
    s.sport_name
FROM SportsDB.Player p
INNER JOIN SportsDB.Team t ON p.team_id = t.team_id
INNER JOIN SportsDB.Sport s ON t.sport_id = s.sport_id
WHERE s.sport_name = 'Foot Ball'
  AND p.player_salary > 200000;