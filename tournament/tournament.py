"""
Copyright 2015 Brian Quach
Licensed under MIT (https://github.com/brianquach/udacity-nano-fullstack-tournament/blob/master/LICENSE)  # noqa
"""
import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    c = conn.cursor()
    c.execute("DELETE FROM match")
    c.execute("DELETE FROM match_tie")
    conn.commit()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    c = conn.cursor()
    c.execute("DELETE FROM player")
    conn.commit()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT COUNT(id) FROM player")
    row = c.fetchone()
    conn.close()
    return row[0] if row is not None else 0


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).

    Returns:
      Newly registered player's Id
    """
    conn = connect()
    c = conn.cursor()
    tournament_id = activeTournamentId()
    c.execute("INSERT INTO player (name, tournamentId) VALUES (%s, %s) "
              "RETURNING id", (name, tournament_id))
    player_id = c.fetchone()[0]
    conn.commit()
    conn.close()
    return player_id


def playerStandings(include_ties=False):
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a
    player tied for first place if there is currently a tie. Optional parameter
    include_ties added in for backwards compatability with original test cases
    from the code fork.

    Args:
      include_ties: if true return the number of ties to the tuple being
        returned.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
        ties (optional): the number of matches the player has tied
    """
    conn = connect()
    c = conn.cursor()
    if include_ties:
        c.execute("SELECT * FROM playerStandingWithTies")
    else:
        c.execute("SELECT * FROM playerStanding")
    player_standings = c.fetchall()
    conn.close()
    return player_standings


def reportMatch(winner, loser, is_tie=False):
    """Records the outcome of a single match between two players.

    Args:
      winner: the id number of the player who won
      loser: the id number of the player who lost
      is_tie: true if the match ended in a tie, otherwise false
    """
    conn = connect()
    c = conn.cursor()
    tournament_id = activeTournamentId()
    if is_tie:
        c.execute("INSERT INTO match_tie (playerOneId, playerTwoId) VALUES "
                  "(%s, %s) RETURNING id", (winner, loser))
        tie_id = c.fetchone()[0]
        c.execute("INSERT INTO match (tournamentId, tieId) VALUES "
                  "(%s, %s)", (tournament_id, tie_id))
    else:
        c.execute("INSERT INTO match (tournamentId, winnerId, loserId) VALUES "
                  "(%s, %s, %s)", (tournament_id, winner, loser))
    conn.commit()
    conn.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    pairings = []
    standings = playerStandings()
    index = 0
    player_count = len(standings)
    while index < player_count:
        player_one = standings[index]
        index += 1
        if (index < player_count):
            player_two = standings[index]
            pairings.append((
                player_one[0],
                player_one[1],
                player_two[0],
                player_two[1]
            ))
        else:
            pairings.push((player_one[0], player_one[1], None, None))
        index += 1
    return pairings


def createTournament():
    """Creates a new tournament and returns its id."""
    conn = connect()
    c = conn.cursor()
    c.execute("INSERT INTO tournament (id) VALUES (DEFAULT) RETURNING id")
    tournament_id = c.fetchone()[0]
    conn.commit()
    conn.close()
    return tournament_id


def deleteTournaments():
    """Remove all tournament records from the database."""
    conn = connect()
    c = conn.cursor()
    c. execute("DELETE FROM tournament")
    conn.commit()
    conn.close()


def activeTournamentId():
    """Returns the active tournament Id.

    An active tournament is the most recent tournament where players are still
    playing with no winner. If there are no tournaments then a new one will be
    created and its id returned.
    """
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT id FROM tournament ORDER BY id DESC LIMIT 1")
    row = c.fetchone()
    tournament_id = createTournament() if row is None else row[0]
    conn.close()
    return tournament_id
