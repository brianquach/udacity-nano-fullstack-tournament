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
CREATE TABLE outcome (
    id serial PRIMARY KEY,
    winnerId integer REFERENCES player(id),
    loserId integer REFERENCES player(id),
    isTie boolean NULL
);
CREATE TABLE match (
    id serial PRIMARY KEY,
    roundNumber integer NOT NULL,
    playerOneId integer REFERENCES player(id), 
    playerTwoId integer REFERENCES player(id),
    outcomeId integer REFERENCES outcome(id)
);

-- View definitions
-- CREATE VIEW playerStanding AS (
--     SELECT p.id, COUNT(o.winnder) as wins, as losses, as ties, p.tournamentId
--     FROM player p, match m, outcome o
--     WHERE (p.id = m.playerOneId OR p.id = m.playerTwoId) 
--         AND (p.tournamentId = m.tournamentId)
--         AND (m.outcomeId = o.id)
--     GROUP BY p.tournamentId, p.id
-- );