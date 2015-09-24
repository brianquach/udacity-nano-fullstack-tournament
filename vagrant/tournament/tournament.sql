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
    winnerId integer REFERENCES player(id), 
    loserId integer REFERENCES player(id)
);

-- View definitions
CREATE VIEW playerStanding AS (
    SELECT p.id, p.name, COUNT(m.winnerId) AS wins, COUNT(m.winnerId) + COUNT(m2.loserID) AS matches
    FROM player p
        LEFT JOIN match m ON p.id = m.winnerId
        LEFT JOIN match m2 ON p.id = m2.loserId
    GROUP BY p.id, m.winnerId, m2.loserId
    ORDER BY wins DESC
);
