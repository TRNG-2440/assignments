SELECT p.player_name, p.player_salary
FROM Player p
JOIN Team t
    ON p.team_id = t.team_id
JOIN Sport s
    ON t.sport_id = s.sport_id
WHERE s.sport_name = 'Foot Ball'
  AND p.player_salary > 200000;