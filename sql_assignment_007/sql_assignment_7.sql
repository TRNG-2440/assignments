WITH highest_paid_player_cte AS (
    SELECT p.*
    FROM Player p
    WHERE player_salary = (
        SELECT MAX(player_salary)
        FROM Player
    )
)

SELECT s.sport_name
FROM Team t 
JOIN highest_paid_player_cte h USING(team_id)
JOIN Sport s USING(sport_id);