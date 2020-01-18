import json
import os

from dao import DataWriter, GamesDao
from apicall import ApiCall

DOTABUFFURL = "https://www.dotabuff.com/matches/%d"
BROKEGAMES = [5036395844, 5098676102]
dotaApi = ApiCall()

captains = []
allCaptains = []
with open(os.getcwd() + r"\io\static\Captains.txt", "r") as captxt:
    seas = []
    for line in captxt:
        if "Season" in line and len(seas) > 0:
            captains.append(seas.copy())
            seas.clear()
        if "Season" not in line:
            allCaptains.append(int(line.strip()))
            seas.append(int(line.strip()))

MISSED_GAME = []
with open(os.getcwd() + r"\io\static\missedGames.txt", "r") as missedtxt:
    seas = []
    for line in missedtxt:
        if "Season" in line and len(seas) > 0:
            MISSED_GAME.append(seas.copy())
            seas.clear()
        if "Season" not in line:
            seas.append(int(line.strip()))

class CDL():

    def __init__(self, leagueIds):
        self.seasons = []
        for league in leagueIds:
            self.seasons.append(Season(league[1], league[0]))


class Season():

    def __init__(self, seasonId, seasonNumber):
        self.matches = []
        self.seasonId = seasonId
        self.seasonNumber = seasonNumber
        resp = dotaApi.getLeague(league_id=seasonId)
        print("{0} matches parsing...".format(len(resp)))
        for index, match in enumerate(resp):
            matchId = match['match_id']
            if matchId not in BROKEGAMES and self.checkForMatch(matchId):
                print('\r%d' % (index), end='')
                match["seasonNumber"] = seasonNumber
                self.matches.append(Match(match))

    def checkForMatch(self, matchId):
        gamesColl = GamesDao("games")
        if len(gamesColl.lookForMatch(matchId)) > 0:
            return False
        return True

    def formatMatches(self):
        formattedMatches = []
        for match in self.matches:
            formattedMatches.append(match.__dict__)
        return formattedMatches

    def formatPerformances(self):
        perf = []
        for match in self.matches:
            perf = perf + match.formatPerformances()
        return perf


class Match():
    def __init__(self, matchId):
        self.players = []
        self.matchId = matchId['match_id']
        match = dotaApi.getMatch(match_id=self.matchId)
        self.seasonNumber = matchId["seasonNumber"]
        for point in match:
            self.__setattr__(point, match[point])
        for perf in self.players:
            realSteamId = perf["account_id"] + 76561197960265728
            perf["steamName"] = dotaApi.getPlayerName(steamids=realSteamId)
            team = self.checkTeam(perf)
            if match["radiant_win"] and team == 'rad' or not match["radiant_win"] and team == 'dire':
                perf["win"] = 1
            else:
                perf["win"] = 0
            if perf["account_id"] in captains[self.seasonNumber - 1]:
                perf["captain"+str(self.seasonNumber)] = 1
                perf["seasonCaptain"] = 1
            if perf["account_id"] in allCaptains:
                perf["captain"] = 1

    def formatPerformances(self):
        performances = []
        for perf in self.players:
            perf["dotabuff"] = DOTABUFFURL % (self.matchId)
            perf["match_id"] = self.matchId
            perf["seasonNumber"] = self.seasonNumber
            performances.append(perf)
        return performances

    def checkTeam(self, player):
        if player["player_slot"] < 5:
            return 'rad'
        else:
            return 'dire'


# for testing purposes
if __name__ == "__main__":
    print(MISSED_GAME)
