/*
Copyright 2015 Brian Quach
Licensed under MIT (https://github.com/brianquach/udacity-nano-fullstack-tournament/blob/master/LICENSE)
*/
-- Ensure fresh database scheme
DROP DATABASE tournament;
CREATE DATABASE tournament;
\c tournament;

-- Table definitions
CREATE TABLE tournament (
    id serial PRIMARY KEY
);
CREATE TABLE player (
    id serial PRIMARY KEY,
    name varchar(1000) NOT NULL,
    tournamentId integer REFERENCES tournament(id)
);
CREATE TABLE match (
    id serial PRIMARY KEY,
    tournamentId integer REFERENCES tournament(id),
    winnerId integer REFERENCES player(id) NULL, 
    loserId integer REFERENCES player(id) NULL,
    isTie boolean
);
CREATE TABLE match_tie (
    matchId integer REFERENCES match(id),
    playerId integer REFERENCES player(id)
);

-- View definitions
CREATE VIEW playerStandingBasic AS (
    SELECT p.id, p.name, COUNT(m.winnerId) AS wins, COUNT(m.winnerId) + COUNT(m2.loserID) AS matches
    FROM player p
        LEFT JOIN match m ON p.id = m.winnerId
        LEFT JOIN match m2 ON p.id = m2.loserId
    GROUP BY p.id, m.winnerId, m2.loserId
    ORDER BY wins DESC
);
CREATE VIEW playerStandingExpanded AS (
    SELECT p.id, p.name, COUNT(m.winnerId) AS wins, COUNT(m.winnerId) + COUNT(m2.loserID) + COUNT(mt.playerId) AS matches, COUNT(mt.playerId) AS ties, p.tournamentId
    FROM player p
        LEFT JOIN match m ON p.id = m.winnerId
        LEFT JOIN match m2 ON p.id = m2.loserId
        LEFT JOIN match_tie mt ON p.id = mt.playerId
    GROUP BY p.tournamentId, p.id, m.winnerId, m2.loserId, mt.playerId
    ORDER BY wins DESC
);
