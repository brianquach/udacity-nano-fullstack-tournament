"""
The original author of this code is Udacity's Full-Stack Web Developer
Nanodegree course.
Code modified by: Brian Quach (13rianquach@gmail.com)
"""
from tournament import *


def testDeleteMatches():
    deleteMatches()
    print "1. Old matches can be deleted."


def testDelete():
    deleteMatches()
    deletePlayers()
    print "2. Player records can be deleted."


def testCount():
    deleteMatches()
    deletePlayers()
    c = countPlayers()
    if c == '0':
        raise TypeError(
            "countPlayers() should return numeric zero, not string '0'."
        )
    if c != 0:
        raise ValueError("After deleting, countPlayers should return zero.")
    print "3. After deleting, countPlayers() returns zero."


def testRegister():
    deleteMatches()
    deletePlayers()
    registerPlayer("Chandra Nalaar")
    c = countPlayers()
    if c != 1:
        raise ValueError(
            "After one player registers, countPlayers() should be 1."
        )
    print "4. After registering a player, countPlayers() returns 1."


def testRegisterCountDelete():
    deleteMatches()
    deletePlayers()
    registerPlayer("Markov Chaney")
    registerPlayer("Joe Malik")
    registerPlayer("Mao Tsu-hsi")
    registerPlayer("Atlanta Hope")
    c = countPlayers()
    if c != 4:
        raise ValueError(
            "After registering four players, countPlayers should be 4."
        )
    deletePlayers()
    c = countPlayers()
    if c != 0:
        raise ValueError("After deleting, countPlayers should return zero.")
    print "5. Players can be registered and deleted."


def testStandingsBeforeMatches():
    deleteMatches()
    deletePlayers()
    registerPlayer("Melpomene Murray")
    registerPlayer("Randy Schwartz")
    standings = playerStandings()
    if len(standings) < 2:
        raise ValueError(
            "Players should appear in playerStandings even before they have "
            "played any matches."
        )
    elif len(standings) > 2:
        raise ValueError("Only registered players should appear in standings.")
    if len(standings[0]) != 4:
        raise ValueError("Each playerStandings row should have four columns.")
    [(id1, name1, wins1, matches1), (id2, name2, wins2, matches2)] = standings
    if matches1 != 0 or matches2 != 0 or wins1 != 0 or wins2 != 0:
        raise ValueError(
            "Newly registered players should have no matches or wins.")
    if set([name1, name2]) != set(["Melpomene Murray", "Randy Schwartz"]):
        raise ValueError(
            "Registered players' names should appear in standings, even if "
            "they have no matches played."
        )
    print ("6. Newly registered players appear in the standings with no "
           "matches.")


def testReportMatches():
    deleteMatches()
    deletePlayers()
    registerPlayer("Bruno Walton")
    registerPlayer("Boots O'Neal")
    registerPlayer("Cathy Burton")
    registerPlayer("Diane Grant")
    standings = playerStandings()
    [id1, id2, id3, id4] = [row[0] for row in standings]
    reportMatch(id1, id2)
    reportMatch(id3, id4)
    standings = playerStandings()
    for (i, n, w, m) in standings:
        if m != 1:
            raise ValueError("Each player should have one match recorded.")
        if i in (id1, id3) and w != 1:
            raise ValueError("Each match winner should have one win recorded.")
        elif i in (id2, id4) and w != 0:
            raise ValueError(
                "Each match loser should have zero wins recorded."
            )
    print "7. After a match, players have updated standings."


def testPairings():
    deleteMatches()
    deletePlayers()
    registerPlayer("Twilight Sparkle")
    registerPlayer("Fluttershy")
    registerPlayer("Applejack")
    registerPlayer("Pinkie Pie")
    standings = playerStandings()
    [id1, id2, id3, id4] = [row[0] for row in standings]
    reportMatch(id1, id2)
    reportMatch(id3, id4)
    pairings = swissPairings()
    if len(pairings) != 2:
        raise ValueError(
            "For four players, swissPairings should return two pairs."
        )
    [(pid1, pname1, pid2, pname2), (pid3, pname3, pid4, pname4)] = pairings
    correct_pairs = set([frozenset([id1, id3]), frozenset([id2, id4])])
    actual_pairs = set([frozenset([pid1, pid2]), frozenset([pid3, pid4])])
    if correct_pairs != actual_pairs:
        raise ValueError(
            "After one match, players with one win should be paired."
        )
    print "8. After one match, players with one win are paired."


# Add my own test cases below
def testDeleteTournaments():
    deleteMatches()
    deletePlayers()
    deleteTournaments()
    print "9. Tournaments can be deleted."


def testTournamentFunctions():
    deleteTournaments()
    tournament_id = createTournament()
    if type(tournament_id) != int:
        raise ValueError(
            "After creating the first tournament, createTournament() should "
            "return an integer."
        )
    active_tournament_id = activeTournamentId()
    if tournament_id != active_tournament_id:
        raise ValueError(
            "After creating tournament, activeTournamentId() should return "
            "the Id of the created tournament."
        )
    print ("10. After creating a tournament, activeTournamentId() returns the "
           "created tournament Id.")


def testReportMatchTie():
    deleteMatches()
    deletePlayers()
    deleteTournaments()
    id1 = registerPlayer("Luis Lagos")
    id2 = registerPlayer("Brian Quach")
    reportMatch(id1, id2, True)
    standings = playerStandings(True)
    for (tId, i, n, w, l, t, m, omw) in standings:
        if m != 1:
            raise ValueError("Each player should have one match recorded.")
        if w != 0:
            raise ValueError(
                "Each player should have zero win recorded."
            )
        if t != 1:
            raise ValueError(
                "Each player should have one tie recorded"
            )
    print "11. After one match each player has a tie."


def testBye():
    deleteMatches()
    deletePlayers()
    deleteTournaments()
    createTournament()
    id1 = registerPlayer("Macky Mac")
    pairings = swissPairings()
    if not doesPlayerHaveBye(id1):
        raise ValueError(
            "After pairings, since only one player, doesPlayerHaveBye() should"
            " return True"
        )
    print ("12. After pairings, since only one player, doesPlayerHaveBye() "
           "returns True.")


def testPlayerStandingsWithOpponentMatchWins():
    deleteMatches()
    deletePlayers()
    deleteTournaments()
    id1 = registerPlayer("A")
    id2 = registerPlayer("B")
    id3 = registerPlayer("C")
    id4 = registerPlayer("D")
    id5 = registerPlayer("E")
    id6 = registerPlayer("F")
    id7 = registerPlayer("G")
    id8 = registerPlayer("H")
    id9 = registerPlayer("I")
    id10 = registerPlayer("J")
    id11 = registerPlayer("K")
    id12 = registerPlayer("L")
    id13 = registerPlayer("M")
    id14 = registerPlayer("N")
    id15 = registerPlayer("O")

    # First Round
    reportMatch(id1, id2)
    reportMatch(id3, id4)
    reportMatch(id5, id6)
    reportMatch(id7, id8)
    reportMatch(id9, id10)
    reportMatch(id11, id12)
    reportMatch(id13, id14, True)
    reportMatch(id15, None)

    # Second Round
    reportMatch(id1, id3)
    reportMatch(id7, id5)
    reportMatch(id9, id11)
    reportMatch(id13, id15, True)
    reportMatch(id2, id4)
    reportMatch(id8, id6)
    reportMatch(id10, id12)
    reportMatch(id14, None)

    # Third Round
    reportMatch(id7, id1)
    reportMatch(id9, id15)
    reportMatch(id14, id2)
    reportMatch(id3, id5)
    reportMatch(id10, id8)
    reportMatch(id13, id11)
    reportMatch(id4, id12, True)
    reportMatch(id6, None)

    # Final Round
    reportMatch(id7, id9, True)
    reportMatch(id14, id1)
    reportMatch(id3, id10, True)
    reportMatch(id13, id8)
    reportMatch(id15, id11)
    reportMatch(id2, id5)
    reportMatch(id4, id6, True)
    reportMatch(id12, None)

    player_standings = playerStandings(True)
    [p1, p2, p3, p4, p5, p6, p7, p8,
     p9, p10, p11, p12, p13, p14, p15] = [row for row in player_standings]
    if p1[1] != "I" and p1[7] != 35:
        raise ValueError("Player I should be first with OMW of 35")
    if p2[1] != "G" and p2[7] != 29:
        raise ValueError("Player I should be second with OMW of 29")
    if p3[1] != "N" and p3[7] != 26:
        raise ValueError("Player I should be third with OMW of 26")
    if p4[1] != "M" and p4[7] != 30:
        raise ValueError("Player I should be forth with OMW of 30")
    if p5[1] != "J" and p5[7] != 31:
        raise ValueError("Player A should be fifth with OMW of 31")
    if p6[1] != "O" and p6[7] != 27:
        raise ValueError("Player I should be sixth with OMW of 27")
    if p7[1] != "C" and p7[7] != 23:
        raise ValueError("Player I should be seventh with OMW of 23")
    if p8[1] != "A" and p8[7] != 43:
        raise ValueError("Player I should be eighth with OMW of 43")
    if p9[1] != "B" and p9[7] != 27:
        raise ValueError("Player I should be ninth with OMW of 27")
    if p10[1] != "L" and p10[7] != 15:
        raise ValueError("Player I should be tenth with OMW of 15")
    if p11[1] != "F" and p11[7] != 10:
        raise ValueError("Player I should be eleventh with OMW of 10")
    if p12[1] != "K" and p12[7] != 37:
        raise ValueError("Player I should be twelfth with OMW of 37")
    if p13[1] != "H" and p13[7] != 37:
        raise ValueError("Player I should be thirteenth with OMW of 37")
    if p14[1] != "E" and p14[7] != 35:
        raise ValueError("Player D should be fourteenth with OMW of 35")
    if p15[1] != "D" and p15[7] != 27:
        raise ValueError("Player I should be fifteenth with OMW of 27")
    print (
        "13. After a full swiss-tournament players are ranked from first to "
        "last as follows: I, G, N, M, J, O, C, A, B, L, F, K, H, E, D."
    )


def testPreventRematch():
    deleteMatches()
    deletePlayers()
    deleteTournaments()
    id1 = registerPlayer("Jim Raynor")
    id2 = registerPlayer("Mengus Minsk")
    id3 = registerPlayer("Arnold Shortman")
    id4 = registerPlayer("Frank Sanatra")

    reportMatch(id1, id2)
    reportMatch(id2, id1)
    reportMatch(id3, id4)
    reportMatch(id4, id3)
    reportMatch(id1, id2)
    reportMatch(id2, id4)

    swissPairings()
    if not havePlayersBeenPaired(id1, id2):
        raise ValueError(
            "Players Jim Raynor and player Mengus Minsk have already been "
            "paired; havePlayersBeenPaired() should return True"
        )

    print ("14. Rematch prevented until a player has played against everyone "
           "else.")

if __name__ == '__main__':
    testDeleteMatches()
    testDelete()
    testCount()
    testRegister()
    testRegisterCountDelete()
    testStandingsBeforeMatches()
    testReportMatches()
    testPairings()
    testDeleteTournaments()
    testTournamentFunctions()
    testReportMatchTie()
    testBye()
    testPlayerStandingsWithOpponentMatchWins()
    testPreventRematch()
    print "Success!  All tests pass!"
