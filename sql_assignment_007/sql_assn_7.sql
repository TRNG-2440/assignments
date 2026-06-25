SELECT S.sport_name
FROM Player P
INNER JOIN Team T ON T.team_id = P.team_id
INNER JOIN Sport S ON S.sport_id = T.sport_id
WHERE P.player_salary = (
    SELECT MAX(player_salary)
    FROM Player;
);