SELECT p.player_name FROM Player p
JOIN Team t ON p.team_id = t.team_id
WHERE p.`player Salary` > 200000 AND t.sport_id = 40001;