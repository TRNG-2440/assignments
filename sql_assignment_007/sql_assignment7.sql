SELECT
    s.sport_name,
    MAX(p.player_salary) AS highest_salary
FROM player AS p
    INNER JOIN team AS t
        ON p.team_id = t.team_id
    INNER JOIN sport AS s
        ON t.sport_id = s.sport_id
GROUP BY
    s.sport_name
ORDER BY
    highest_salary DESC
LIMIT 1;
