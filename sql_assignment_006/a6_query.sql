-- subquery
SELECT player_name
FROM player 
WHERE player_salary > 200000
AND team_id IN (SELECT team_id 
    FROM team 
    WHERE sport_id IN (SELECT sport_id 
        FROM sport 
        WHERE sport_name = 'Football'));

-- join statement
SELECT player.player_name
FROM player
JOIN team ON player.team_id = team.team_id
JOIN sport ON team.sport_id = sport.sport_id
WHERE sport.sport_name = 'Football'
AND player.player_salary > 200000;