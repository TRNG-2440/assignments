-- assuume player name is a typo and _ is required
-- assume over 200,000 doesn't include 200,000
SELECT p.player_name 'name', p.player_salary 'salary'
FROM player p
JOIN team t ON t.team_id = p.team_id
JOIN sport s ON s.sport_id = t.sport_id
WHERE player_salary > 200000 AND s.sport_name = 'Foot Ball';