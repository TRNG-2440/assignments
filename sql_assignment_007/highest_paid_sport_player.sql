SELECT Sport.sport_name, MAX(Player.player_salary) as highest_paid_player FROM Sport
JOIN Team
    ON Sport.sport_id = Team.sport_id
JOIN Player
    ON Team.team_id = Player.team_id
GROUP BY Sport.sport_name
ORDER BY MAX(Player.player_salary) DESC
LIMIT 1;
