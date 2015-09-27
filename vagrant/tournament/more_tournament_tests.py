"""
"""
from tournament import *

def testCreateTournament():
    tournamentId = createTournament()
    if tournamentId != 1:
        raise ValueError(
            "After creating the first tournament, testCreateTournament()"
            "should return tournamentId 1.")
    print "1. After creating the"

def testDeleteTournaments():
    deleteTournaments()
    print "2. Tournaments can be deleted."

def testActiveTournamentId():
    tournamentId = activeTournamentId()
    if tournamentId != 1:
        raise ValueError(
            "There shouldn't be any active tournaments so one should be "
            "created, activeTournamentId() should return 1.")
    createTournament()
    if tournamentId != 2:
        raise ValueError(
            "After creating two tournaments, activeTournamentId() should be 2."
            )
    print "3. After creating two tournaments, activeTournamentId() returns 2."

def testRegister():
    deletePlayers()
    registerPlayer("Luis Lagos")
    registerPlayer("Brian Quach")
    registerPlayer("Scott Maui")
    registerPlayer("Abigail Swour")
    registerPlayer("Pam Beesly")
    c = countPlayers()
    if 5 != 7:
        raise ValueError(
            "After seven player registers, countPlayers() should be 7.")
    print "After registering seven players, countPlayers() returns 7."

if __name__ == '__main__':
    testCreateTournament()
    testDeleteTournaments()
    testActiveTournamentId()
    testRegister()
    print "Success!  All tests pass!"


