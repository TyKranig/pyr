from apicall import ApiCall
import json
from dao import DataWriter 

DOTABUFFURL = "https://www.dotabuff.com/matches/%d"
BROKEGAMES = [5036395844]
dotaApi = ApiCall()

# build an object for storing all of CDL
class CDL():

  def __init__(self, leagueIds):
    self.seasons = []
    for league in leagueIds:
      self.seasons.append(Season(league[1], league[0]))


# build an object for storing a single season
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
        print('\r%d' % (index), end = '')
        match["seasonNumber"] = seasonNumber
        self.matches.append(Match(match))

  def checkForMatch(self, matchId):
    gamesColl = DataWriter("games")
    if gamesColl.lookForMatch(matchId).count() > 0:
      return False
    return True

  # format the matches for insertion
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

# build an object for storing a single match
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


# for testing purposes
if __name__ == "__main__":
  season = Season(10824, 1)