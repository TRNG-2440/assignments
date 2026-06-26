--SPORTS SCHEMA

DROP SCHEMA IF EXISTS sports CASCADE;

CREATE SCHEMA sports;


--STATES TABLE
CREATE TABLE sports.state(
    state_id SERIAL PRIMARY KEY,
    state_name VARCHAR(255)
);

--SPORTS NAME TABLE
CREATE TABLE sports.sport_name(
    sport_name_id SERIAL PRIMARY KEY,
    sport_name VARCHAR(255)
);

--TEAMS TABLE
CREATE TABLE sports.team(
    team_id SERIAL PRIMARY KEY,
    team_name VARCHAR(255),
    sport_name_id INTEGER,
    state_id INTEGER,

    CONSTRAINT fk_sport_name FOREIGN KEY (sport_name_id) REFERENCES sports.sport_name(sport_name_id),
    CONSTRAINT fk_state FOREIGN KEY (state_id) REFERENCES sports.state(state_id)
    
);


--PLAYERS TABLE
CREATE TABLE sports.player(
    player_id SERIAL PRIMARY KEY,
    player_name VARCHAR(255),
    team_id INTEGER,
    player_salary INTEGER,

    CONSTRAINT fk_team FOREIGN KEY (team_id) REFERENCES sports.team(team_id)

);