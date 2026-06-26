-- CREATE SCHEMA IF NOT EXISTS sports;

-- CREATE TABLE IF NOT EXISTS sports.State(
-- 		state_id INTEGER PRIMARY KEY,
-- 		state_name VARCHAR(100)
-- );

-- CREATE TABLE IF NOT EXISTS sports.Sport(
-- 		sport_id INTEGER PRIMARY KEY,
-- 		sport_name VARCHAR(200)
-- );

-- CREATE TABLE IF NOT EXISTS sports.Team(
-- 		team_id INTEGER PRIMARY KEY,
-- 		team_name VARCHAR(200),
-- 		state_id INTEGER,
-- 		sport_id INTEGER,

-- 		CONSTRAINT state_id_fk FOREIGN KEY (state_id) REFERENCES sports.State(state_id),
-- 		CONSTRAINT sport_id_fk FOREIGN KEY (sport_id) REFERENCES sports.Sport(sport_id)
-- );

-- CREATE TABLE IF NOT EXISTS sports.Player(
-- 		player_id INTEGER PRIMARY KEY,
-- 		team_id INTEGER,
-- 		player_name VARCHAR(300),
-- 		player_salary NUMERIC,

-- 		CONSTRAINT team_id_fk FOREIGN KEY (team_id) REFERENCES sports.Team(team_id)
-- );

-- INSERT INTO sports.State VALUES (10001, 'New York');
-- INSERT INTO sports.State VALUES (10002, 'Texas');
-- INSERT INTO sports.State VALUES (10003, 'Colorado');
-- INSERT INTO sports.State VALUES (10004, 'Florida');
-- INSERT INTO sports.State VALUES (10005, 'California');

-- INSERT INTO sports.Sport VALUES (40001, 'Foot Ball');
-- INSERT INTO sports.Sport VALUES (40002, 'Basket Ball');

-- INSERT INTO sports.Team VALUES (20001, 'Los Angeles Clippers', 10005, 40002);
-- INSERT INTO sports.Team VALUES (20002, 'Denver Broncos', 10003, 40001);
-- INSERT INTO sports.Team VALUES (20003, 'New York Knicks', 10001, 40002);
-- INSERT INTO sports.Team VALUES (20004, 'Miami Dolphins', 10004, 40001);
-- INSERT INTO sports.Team VALUES (20005, 'Denver Nuggets', 10003, 40002);
-- INSERT INTO sports.Team VALUES (20006, 'Dallas Mavericks', 10002, 40002);
-- INSERT INTO sports.Team VALUES (20007, 'Dallas Cowboys', 10002, 40001);
-- INSERT INTO sports.Team VALUES (20008, 'San Francisco 49ers', 10005, 40001);
-- INSERT INTO sports.Team VALUES (20009, 'Miami Heat', 10004, 40002);
-- INSERT INTO sports.Team VALUES (20010, 'Buffalo Bills', 10001, 40001);

-- INSERT INTO sports.Player VALUES (30001, 20006, 'Terry Lennie', 185000);
-- INSERT INTO sports.Player VALUES (30002, 20002, 'Ellis Sidney', 101000);
-- INSERT INTO sports.Player VALUES (30003, 20001, 'Alex Meredith', 236000);
-- INSERT INTO sports.Player VALUES (30004, 20003, 'Parker Lindsay', 240000);
-- INSERT INTO sports.Player VALUES (30005, 20008, 'Lindsey Darian', 241000);
-- INSERT INTO sports.Player VALUES (30006, 20007, 'Kit Stacy', 220000);
-- INSERT INTO sports.Player VALUES (30007, 20003, 'Sammie Hadley', 112000);
-- INSERT INTO sports.Player VALUES (30008, 20003, 'Tracey Bailey', 128000);

SELECT p.player_id, p.player_name as "Player Name", p.player_salary AS "Player Salary"
FROM sports.Player AS p
JOIN sports.Team AS t ON p.team_id = t.team_id
JOIN sports.Sport AS s ON t.sport_id = s.sport_id
WHERE s.sport_name = 'Foot Ball'
AND p.player_salary > 200000;
