"""
Copyright 2015 Brian Quach
Licensed under MIT (https://github.com/brianquach/udacity-nano-fullstack-tournament/blob/master/LICENSE)  # noqa
"""
import random
import psycopg2
from contextlib import contextmanager


@contextmanager
def get_cursor():
    """Returns a context manager that will handle our database connection"""
    conn = connect()
    c = conn.cursor()
    try:
        yield c
    except:
        raise
    else:
        conn.commit()
    finally:
        c.close()
        conn.close()


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    with get_cursor() as c:
        c.execute("TRUNCATE match RESTART IDENTITY CASCADE")


def deletePlayers():
    """Remove all the player records from the database."""
    with get_cursor() as c:
        c.execute("TRUNCATE player RESTART IDENTITY CASCADE")


def countPlayers():
    """Returns the number of players currently registered."""
    with get_cursor() as c:
        c.execute("SELECT COUNT(id) FROM player")
        row = c.fetchone()
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
    tournament_id = activeTournamentId()
    with get_cursor() as c:
        c.execute("INSERT INTO player (name, tournamentId) VALUES (%s, %s) "
                  "RETURNING id", (name, tournament_id))
        player_id = c.fetchone()[0]
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

    # The reason why there are two queries below is that one is used to pass
    # the original Udacity tests, therefore keeping backward compatibily. And
    # other is used for everything else.

    tournament_id = activeTournamentId()
    if show_all_columns:
        query = "SELECT * FROM player_standing WHERE tournamentId = %s"
    else:
        query = """SELECT id, name, wins, matches FROM player_standing WHERE
                tournamentId = %s"""
    with get_cursor() as c:
        c.execute(query, (tournament_id,))
        player_standings = c.fetchall()
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
    tournament_id = activeTournamentId()
    with get_cursor() as c:
        if is_tie:
            c.execute(
                "INSERT INTO match (tournamentId, isTie) VALUES"
                "(%s, %s) RETURNING id", (tournament_id, is_tie)
            )
            match_id = c.fetchone()[0]
            c.execute(
                "INSERT INTO match_tie (matchId, playerId) VALUES "
                "(%s, %s), (%s, %s)", (match_id, winner, match_id, loser)
            )
        else:
            c.execute(
                "INSERT INTO match (tournamentId, winnerId, loserId, isTie) "
                "VALUES (%s, %s, %s, %s) RETURNING id", (
                    tournament_id, winner, loser, is_tie
                )
            )


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
    players = playerStandings(True)
    index = 0
    player_count = len(players)
    is_player_count_odd = (player_count % 2) != 0
    if player_count == 0:
        return []

    matchCount = players[0][6]
    if matchCount == 0:
        random.shuffle(players)

    # If there is an odd number of players, a player will be chosen starting
    # from the top and moving downwards until a player with no 'byes' is found,
    # to be given a bye. The rest of the players will then be paired.

    if is_player_count_odd:
        player_with_bye = None
        for player in players:
            if not doesPlayerHaveBye(player[1]):
                reportMatch(player[1], None, False)
                player_with_bye = player
                break
        if player_with_bye is not None:
            players.remove(player_with_bye)

    while len(players) > 0:
        player1 = players.pop()
        player2 = players.pop()

        # If two players have already played against each other, look down the
        # list of players [higher ranked] until two players are found who have
        # not yet played against each other. Only if a player has played
        # against everyone down the list will a rematch be allowed.

        if havePlayersBeenPaired(player1[1], player2[1]):
            new_pair_found = False
            players.append(player2)
            for i in range((len(players) - 2), -1, -1):
                player2 = players[i]
                if not havePlayersBeenPaired(player1[1], player2[1]):
                    players.remove(player2)
                    new_pair_found = True
                    break
            if not new_pair_found:
                player2 = players.pop()
        pairings.append((player1[1], player1[2], player2[1], player2[2]))

    return pairings


def createTournament():
    """Creates a new tournament and returns its id."""
    with get_cursor() as c:
        c.execute("INSERT INTO tournament (id) VALUES (DEFAULT) RETURNING id")
        tournament_id = c.fetchone()[0]
    return tournament_id


def deleteTournaments():
    """Remove all tournament records from the database."""
    with get_cursor() as c:
        c. execute("TRUNCATE tournament RESTART IDENTITY CASCADE")


def activeTournamentId():
    """Returns the active tournament Id.

    An active tournament is the most recent tournament where players are still
    playing with no winner. If there are no tournaments then a new one will be
    created and its id returned.
    """
    with get_cursor() as c:
        c.execute("SELECT id FROM tournament ORDER BY id DESC LIMIT 1")
        row = c.fetchone()
        tournament_id = createTournament() if row is None else row[0]
    return tournament_id


def doesPlayerHaveBye(player):
    """Determine if a player has a bye in the current tournament.

    Args:
      player: id of player to check for bye.

    Returns:
      A boolean; True if player has a bye in this active tournament, otherwise
      False.
    """
    tournament_id = activeTournamentId()
    with get_cursor() as c:
        c.execute(
            "SELECT * FROM player_bye WHERE tournamentId = %s AND "
            "winnerId = %s", (tournament_id, player)
        )
        row = c.fetchone()
    return row is not None


def havePlayersBeenPaired(player1, player2):
    """Determine if two players have matched against each other already.

    Args:
      player1: id of a player to check
      player2: id of a player to check

    Returns:
      A boolean; True if player1 has already played player2 and vice versa,
      otherwise False.
    """
    tournament_id = activeTournamentId()
    with get_cursor() as c:
        c.execute(
            "SELECT * FROM player_opponents WHERE tournamentId = %s AND "
            "id = %s AND opponentId = %s", (tournament_id, player1, player2)
        )
        row = c.fetchone()
    return row is not None
