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
CREATE TABLE match_tie (
    id serial PRIMARY KEY,
    playerOneId integer REFERENCES player(id),
    playerTwoId integer REFERENCES player(id)
);
CREATE TABLE match (
    id serial PRIMARY KEY,
    tournamentId integer REFERENCES tournament(id),
    winnerId integer REFERENCES player(id) NULL, 
    loserId integer REFERENCES player(id) NULL,
    tieId integer REFERENCES match_tie(id) NULL
);

-- View definitions
CREATE VIEW playerStanding AS (
    SELECT p.id, p.name, COUNT(m.winnerId) AS wins, COUNT(m.winnerId) + COUNT(m2.loserID) + COUNT(mt.id) AS matches
    FROM player p
        LEFT JOIN match m ON p.id = m.winnerId
        LEFT JOIN match m2 ON p.id = m2.loserId
        LEFT JOIN match_tie mt ON p.id = mt.playerOneId OR p.id = mt.playerTwoId
    GROUP BY p.id, m.winnerId, m2.loserId, mt.id
    ORDER BY wins DESC
);
CREATE VIEW playerStandingWithTies AS (
    SELECT p.id, p.name, COUNT(m.winnerId) AS wins, COUNT(m.winnerId) + COUNT(m2.loserID) + COUNT(mt.id) AS matches, COUNT(mt.id) AS ties
    FROM player p
        LEFT JOIN match m ON p.id = m.winnerId
        LEFT JOIN match m2 ON p.id = m2.loserId
        LEFT JOIN match_tie mt ON p.id = mt.playerOneId OR p.id = mt.playerTwoId
    GROUP BY p.id, m.winnerId, m2.loserId, mt.id
    ORDER BY wins DESC
);