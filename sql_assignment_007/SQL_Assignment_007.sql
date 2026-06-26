SELECT sport_name 
FROM Sport 
WHERE sport_id = ( 
    SELECT sport_id FROM Team 
    WHERE team_id IN (
        SELECT team_id FROM Player 
        WHERE player_salary =(
            SELECT MAX(player_salary) FROM Player
        )))
