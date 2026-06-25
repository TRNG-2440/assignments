SELECT player_name
FROM Player P
INNER JOIN Team T ON T.team_id = P.team_id
INNER JOIN Sport S ON S.sport_id = T.sport_id
WHERE S.sport_name = "Foot Ball" AND P.player_salary > 200000; 