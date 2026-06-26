-- --Mark White
-- 2026-06-26
-- Assignment#7

-- SQL Statement to find the sport with the hightest player salary

SELECT s.sport_name
FROM sports.player p
JOIN sports.team t
    ON p.team_id = t.team_id
JOIN sports.sport_name s
    ON t.sport_name_id = s.sport_name_id
WHERE p.player_salary = (
    SELECT MAX(player_salary)
    FROM sports.player
);