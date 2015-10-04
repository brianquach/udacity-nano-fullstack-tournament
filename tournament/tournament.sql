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
CREATE VIEW playerStanding AS (
    SELECT 
        p.tournamentId,
        p.id, 
        p.name,
        COALESCE(w.wins, 0) wins,
        COALESCE(l.losses, 0) losses,
        COALESCE(t.ties, 0) ties,
        COALESCE(w.wins, 0) + COALESCE(l.losses, 0) + COALESCE(t.ties, 0) matches
    FROM player p
        LEFT JOIN (SELECT winnerId, COUNT(winnerId) wins
            FROM match
            GROUP BY winnerId
        ) w ON p.id = w.winnerId
        LEFT JOIN (SELECT loserId, COUNT(loserId) losses
            FROM match
            GROUP BY loserId
        ) l ON p.id = l.loserId 
        LEFT JOIN (SELECT playerId, COUNT(playerId) ties
            FROM match_tie
            GROUP BY playerId
        ) t ON p.id = t.playerId
    ORDER BY wins DESC
);