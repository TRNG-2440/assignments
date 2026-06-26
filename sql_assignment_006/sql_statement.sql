-- Mark White
-- 2026-06-26
-- ASSIGNMENT#6

-- This SQL statement will find players who play football with a salary over 200,000.


SELECT p.player_id,
       p.player_name,
       p.player_salary,
       t.team_name,
       s.sport_name
FROM sports.player p
JOIN sports.team t
    ON p.team_id = t.team_id
JOIN sports.sport_name s
    ON t.sport_name_id = s.sport_name_id
WHERE p.player_salary > 200000
  AND s.sport_name = 'Foot Ball';
