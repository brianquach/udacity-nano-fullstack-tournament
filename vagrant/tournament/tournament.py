#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#
import psycopg2

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    c = conn.cursor()
    c.execute("DELETE FROM match")
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
    """
    conn = connect()
    c = conn.cursor()
    tournamentId = currentTournamentId()
    c.execute("INSERT INTO player (name, tournamentId) VALUES (\'{0}\', {1})"
        .format(name, tournamentId))
    conn.commit()
    conn.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a 
    player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
 
 
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

def createTournament():
    """Creates a new tournament and returns its id."""
    conn = connect()
    c = conn.cursor()
    c.execute("INSERT INTO tournament (id) VALUES (DEFAULT) RETURNING id")
    tournamentId = c.fetchone()[0]
    conn.commit()
    conn.close()
    return tournamentId

def currentTournamentId():
    """Returns the active tournament Id.

    An active tournament is the most recent tournament where players are still
    playing with no winner. If there are no tournaments then a new one will be
    created and its id returned.
    """
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT id FROM tournament ORDER BY id DESC LIMIT 1")
    row = c.fetchone()
    tournamentId = createTournament() if row is None else row[0]
    conn.close()
    return tournamentId
