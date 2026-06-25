SELECT player_id, sports.player.team_id, player_name, "player salary" FROM sports.player
	INNER JOIN sports.team ON sports.player.team_id = sports.team.team_id 
	WHERE "player salary" > 200000 
		AND sport_id = 40001