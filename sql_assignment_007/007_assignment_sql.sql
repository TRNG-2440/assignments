SELECT DISTINCT s.sport_name
FROM Sport s
JOIN Team t
    ON s.sport_id = t.sport_id
JOIN Player p
    ON t.team_id = p.team_id
WHERE p.player_salary = (
    SELECT MAX(p2.player_salary)
    FROM Player p2
);