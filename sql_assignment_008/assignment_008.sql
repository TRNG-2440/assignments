-- CREATE SCHEMA IF NOT EXISTS sports2;

-- CREATE TABLE IF NOT EXISTS sports2.State(
-- 		state_id INTEGER PRIMARY KEY,
-- 		state_name VARCHAR(100)
-- );

-- CREATE TABLE IF NOT EXISTS sports2.Sport(
-- 		sport_id INTEGER PRIMARY KEY,
-- 		sport_name VARCHAR(200)
-- );

-- CREATE TABLE IF NOT EXISTS sports2.Team(
-- 		team_id INTEGER PRIMARY KEY,
-- 		team_name VARCHAR(200),
-- 		state_id INTEGER,
-- 		sport_id INTEGER,

-- 		CONSTRAINT state_id_fk FOREIGN KEY (state_id) REFERENCES sports.State(state_id),
-- 		CONSTRAINT sport_id_fk FOREIGN KEY (sport_id) REFERENCES sports.Sport(sport_id)
-- );

-- CREATE TABLE IF NOT EXISTS sports2.Player(
-- 		player_id INTEGER PRIMARY KEY,
-- 		team_id INTEGER,
-- 		player_name VARCHAR(300),
-- 		player_salary INTEGER,

-- 		CONSTRAINT team_id_fk FOREIGN KEY (team_id) REFERENCES sports.Team(team_id)
-- );

-- INSERT INTO sports2.State VALUES (10001, 'New York');
-- INSERT INTO sports2.State VALUES (10002, 'Texas');
-- INSERT INTO sports2.State VALUES (10003, 'Colorado');
-- INSERT INTO sports2.State VALUES (10004, 'Florida');
-- INSERT INTO sports2.State VALUES (10005, 'California');

-- INSERT INTO sports2.Sport VALUES (40001, 'Foot Ball');
-- INSERT INTO sports2.Sport VALUES (40002, 'Basket Ball');

-- INSERT INTO sports2.Team VALUES (20001, 'Los Angeles Clippers', 10005, 40002);
-- INSERT INTO sports2.Team VALUES (20002, 'Denver Broncos', 10003, 40001);
-- INSERT INTO sports2.Team VALUES (20003, 'New York Knicks', 10001, 40002);
-- INSERT INTO sports2.Team VALUES (20004, 'Miami Dolphins', 10004, 40001);
-- INSERT INTO sports2.Team VALUES (20005, 'Denver Nuggets', 10003, 40002);
-- INSERT INTO sports2.Team VALUES (20006, 'Dallas Mavericks', 10002, 40002);
-- INSERT INTO sports2.Team VALUES (20007, 'Dallas Cowboys', 10002, 40001);
-- INSERT INTO sports2.Team VALUES (20008, 'San Francisco 49ers', 10005, 40001);
-- INSERT INTO sports2.Team VALUES (20009, 'Miami Heat', 10004, 40002);
-- INSERT INTO sports2.Team VALUES (20010, 'Buffalo Bills', 10001, 40001);

-- INSERT INTO sports2.Player VALUES (30001, 20006, 'Terry Lennie', 185000);
-- INSERT INTO sports2.Player VALUES (30002, 20002, 'Ellis Sidney', 101000);
-- INSERT INTO sports2.Player VALUES (30003, 20001, 'Alex Meredith', 236000);
-- INSERT INTO sports2.Player VALUES (30004, 20003, 'Parker Lindsay', 240000);
-- INSERT INTO sports2.Player VALUES (30005, 20008, 'Lindsey Darian', 241000);
-- INSERT INTO sports2.Player VALUES (30006, 20007, 'Kit Stacy', 220000);
-- INSERT INTO sports2.Player VALUES (30007, 20003, 'Sammie Hadley', 112000);
-- INSERT INTO sports2.Player VALUES (30008, 20003, 'Tracey Bailey', 128000);
-- INSERT INTO sports2.Player VALUES(30009, 20002, 'Addison Garnet', 105000);
-- INSERT INTO sports2.Player VALUES(30010, 20005, 'Esme Stace', 146000);
-- INSERT INTO sports2.Player VALUES(30011, 20009, 'Kennedy Meredith', 236000);
-- INSERT INTO sports2.Player VALUES(30012, 20004, 'Cortney Harper', 168000);
-- INSERT INTO sports2.Player VALUES(30013, 20002, 'Loren Addison', 189000);
-- INSERT INTO sports2.Player VALUES(30014, 20009, 'Jojo Noel', 233000);
-- INSERT INTO sports2.Player VALUES(30015, 20010, 'Syd Hilary', 132000);
-- INSERT INTO sports2.Player VALUES(30016, 20006, 'Jools Francis', 204000);
-- INSERT INTO sports2.Player VALUES(30017, 20001, 'Beverly Terry', 210000);
-- INSERT INTO sports2.Player VALUES(30018, 20007, 'Sidney Raven', 157000);
-- INSERT INTO sports2.Player VALUES(30019, 20006, 'Page Ricki', 247000);
-- INSERT INTO sports2.Player VALUES(30020, 20003, 'Palmer Beau', 104000);
-- INSERT INTO sports2.Player VALUES(30021, 20008, 'Hadley Lindsey', 133000);
-- INSERT INTO sports2.Player VALUES(30022, 20008, 'Yancy Cameron', 220000);
-- INSERT INTO sports2.Player VALUES(30023, 20010, 'Jo Jools', 140000);
-- INSERT INTO sports2.Player VALUES(30024, 20001, 'Raleigh Ricki', 170000);
-- INSERT INTO sports2.Player VALUES(30025, 20004, 'Tibby Ronnie', 138000);
-- INSERT INTO sports2.Player VALUES(30026, 20009, 'Jules Evelyn', 175000);
-- INSERT INTO sports2.Player VALUES(30027, 20007, 'Lesley Izzy', 179000);
-- INSERT INTO sports2.Player VALUES(30028, 20005, 'Eddie Peyton', 129000);
-- INSERT INTO sports2.Player VALUES(30029, 20010, 'Alpha Jocelyn', 215000);
-- INSERT INTO sports2.Player VALUES(30030, 20004, 'Parker Emery', 202000);

SELECT * FROM sports2.Player WHERE player_name LIKE 'Jo%';
SELECT * FROM sports2.Player WHERE player_name LIKE '%a%e%';
