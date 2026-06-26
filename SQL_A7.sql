SELECT s.sport_name
FROM Player p
JOIN Team t ON p.team_id = t.team_id
JOIN Sport s ON t.sport_id = s.sport_id
WHERE p.`player Salary` = (
    SELECT MAX(`player Salary`) 
    FROM Player
);