SELECT sport_name FROM sports.sport
	WHERE sport_id = (SELECT sport_id FROM sports.player
		INNER JOIN sports.team ON sports.team.team_id = sports.player.team_id
		WHERE "player salary" = (SELECT MAX("player salary") FROM sports.player)
		LIMIT 1)