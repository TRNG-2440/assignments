SELECT Sport.sport_name, Player.player_name, Player.player_salary
FROM Player
JOIN Team
ON Player.team_id = Team.team_id
JOIN Sport
ON Team.sport_id = Sport.sport_id
WHERE Player.player_salary = (
    SELECT MAX(player_salary)
    FROM Player
);