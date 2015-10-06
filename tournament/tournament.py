"""
Copyright 2015 Brian Quach
Licensed under MIT (https://github.com/brianquach/udacity-nano-fullstack-tournament/blob/master/LICENSE)  # noqa
"""
import random
import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    c = conn.cursor()
    c.execute("DELETE FROM match_tie")
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


def playerStandings(show_all_columns=False):
    """Returns a list of the players and their win records, sorted by wins.
    
    Player standings are ranked in descending order first by wins, then ties,
    then Opponent Match Wins (OMW). OMW is the total number of match points 
    based on wins (4 pts) and ties (1pt) by opponents a player has played 
    against. Optional parameter show_all_columns added in for backwards 
    compatability with original test cases from the code fork.

    Opponent Match Wins based off Wizard's OMW:
      https://www.wizards.com/dci/downloads/tiebreakers.pdf

    Args:
      show_all_columns: if true all the columns from playerStanding will be
        returned.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
      Or when show_all_columns is True a list of tupes, each of which contains 
      the above and (tournamentId, losses, ties, omw):
        tournamentId: the tournament's unique id (assigned by the database)
        losses: the number of matches the player has lost
        ties: the number of matches the player has tied
        omw: the total points added up from player's opponent's wins and ties
    """
    conn = connect()
    c = conn.cursor()

    # The reason why there are two queries below is that the 
    # playerStandingBasic is used to pass the original Udacity tests for 
    # backward compatibily. And playerStandingExpanded is used for everything 
    # else.

    tournament_id = activeTournamentId()
    query = "SELECT {0} FROM player_standing WHERE tournamentId = %s".format(
        "*" if show_all_columns else "id, name, wins, matches"
    )
    c.execute(query, (tournament_id,))
    player_standings = c.fetchall()
    conn.close()
    return player_standings


def reportMatch(winner, loser, is_tie=False):
    """Records the outcome of a single match between two players.

    If there is a winner but no loser then the winner has received a 'bye' or a
    free win. A player cannot have more than 'bye' in a tournament.

    Args:
      winner: the id number of the player who won
      loser: the id number of the player who lost
      is_tie: true if the match ended in a tie, otherwise false
    """
    conn = connect()
    c = conn.cursor()
    tournament_id = activeTournamentId()
    if is_tie:
        c.execute(
            "INSERT INTO match (tournamentId, isTie) VALUES"
            "(%s, %s) RETURNING id", (tournament_id, is_tie)
        )   
        match_id = c.fetchone()[0]
        c.execute("INSERT INTO match_tie (matchId, playerId) VALUES "
                  "(%s, %s), (%s, %s)", (match_id, winner, match_id, loser))
    else:
        c.execute(
            "INSERT INTO match (tournamentId, winnerId, loserId, isTie) VALUES"
            "(%s, %s, %s, %s) RETURNING id", (tournament_id, winner, loser, 
                is_tie)
        )
    conn.commit()
    conn.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    If there are an odd number of players, one of the players will receive a
    'bye' if they haven't already; if a player already has a 'bye', then
    another player will be chosen.

    Swiss pairing structured after Wizard's swiss-pairing system:
      http://www.wizards.com/dci/downloads/swiss_pairings.pdf

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    pairings = []
    players = playerStandings()
    index = 0
    player_count = len(players)
    if player_count == 0:
        return []

    matchCount = players[0][3]
    if matchCount == 0:
        random.shuffle(players)

    while index < player_count:
        player_one = players[index]
        index += 1
        if (index < player_count):
            player_two = players[index]
            pairings.append((
                player_one[0],
                player_one[1],
                player_two[0],
                player_two[1]
            ))
        else:
            reportMatch(player_one[0], None, False)  # assign odd player a bye
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


def doesPlayerHaveBye(player):
    """Returns the number of byes a player has in the current tournament.

    Args:
      player: id of player to check for bye.

    Returns:
      A boolean; True if player has a bye in this active tournament, otherwise
      False.
    """
    conn = connect()
    c = conn.cursor()
    tournament_id = activeTournamentId()
    c.execute(
        "SELECT * FROM player_bye WHERE tournamentId = %s AND winnerId = %s",
        (tournament_id, player)
    )
    row = c.fetchone()
    conn.close()
    return row is not None;
