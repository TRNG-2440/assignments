-- Given the following tables, provide an SQL statement that will find which sport has the highest paid player.

select player.player_salary, sport.sport_name from player
join team on team.team_id = player.team_id
join sport on sport.sport_id = team.sport_id
order by player.player_salary desc limit 1;
