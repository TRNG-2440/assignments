SELECT player_name
FROM Player WHERE
player_salary > 200000 AND
team_id IN (SELECT team_id FROM Team WHERE sport_id = (
    SELECT sport_id FROM Sport WHERE sport_name = 'Foot Ball'
));