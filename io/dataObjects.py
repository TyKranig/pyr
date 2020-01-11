import json

from dao import DataWriter
from apicall import ApiCall
from parseCaptains import loadCaptains

DOTABUFFURL = "https://www.dotabuff.com/matches/%d"
BROKEGAMES = [5036395844]
dotaApi = ApiCall()
parsedCaptains = loadCaptains()
captains = []

for capt in loadCaptains():
    captains.append(Captain(capt[0], capt[1]))


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
        gamesColl = DataWriter("games")
        if gamesColl.lookForMatch(matchId).count() > 0:
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
        for player in self.players:
            realSteamId = player["account_id"] + 76561197960265728
            player["steamName"] = dotaApi.getPlayerName(steamids=realSteamId)
            if player["account_id"] in captains:
                captains[captains.index(player["account_id"])].

    def formatPerformances(self):
        performances = []
        for perf in self.players:
            perf["dotabuff"] = DOTABUFFURL % (self.matchId)
            perf["match_id"] = self.matchId
            perf["seasonNumber"] = self.seasonNumber
            performances.append(perf)
        return performances


def Captain():
    def __init__(self, name, id):
        self.name = name
        self.id = id
        self.wins = []

    def __eq__(self, other):
        return other is self.id

    def addToWins(self, season):
        


# for testing purposes
if __name__ == "__main__":
    season = Season(10824, 1)
