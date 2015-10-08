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
CREATE VIEW player_record AS (
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
);
CREATE VIEW player_opponents AS (
    SELECT p.tournamentId, p.id, p.name, m.loserId opponentId, pr.name opponentName, (pr.wins*4) opponentMatchWinPoints, pr.ties opponentMatchTiePoints
    FROM player p
        INNER JOIN match m ON p.id = m.winnerId
        INNER JOIN player_record pr ON m.loserId = pr.id
    WHERE m.loserId IS NOT NULL
    UNION
    SELECT p.tournamentId, p.id, p.name, m.winnerId opponentId, pr.name opponentName, (pr.wins*4) opponentMatchWinPoints, pr.ties opponentMatchTiePoints
    FROM player p
        INNER JOIN match m ON p.id = m.loserId
        INNER JOIN player_record pr ON m.winnerId = pr.id
    WHERE m.winnerId IS NOT NULL
    UNION
    SELECT p.tournamentId, p.id, p.name, mt2.playerId opponentId, pr.name opponentName, (pr.wins*4) opponentMatchWinPoints, pr.ties opponentMatchTiePoints
    FROM player p 
        INNER JOIN match_tie mt ON p.id = mt.playerId 
        INNER JOIN match_tie mt2 ON mt.matchId = mt2.matchId AND mt.playerId != mt2.playerId
        INNER JOIN player_record pr ON mt2.playerId = pr.id
);
CREATE VIEW player_standing AS (
    SELECT pr.*, COALESCE(SUM(po.opponentMatchWinPoints) + SUM(po.opponentMatchTiePoints), 0) omw
    FROM player_record pr
        LEFT JOIN player_opponents po ON pr.id = po.id
    GROUP BY pr.tournamentId, pr.id, pr.name, pr.wins, pr.losses, pr.ties, pr.matches
    ORDER BY pr.wins DESC, pr.ties DESC, omw DESC 
);
CREATE VIEW player_bye AS (
    SELECT m.winnerId, tournamentId
    FROM match m
    WHERE (m.winnerId IS NOT NULL) AND (m.loserId IS NULL)
);