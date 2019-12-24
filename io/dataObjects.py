from apicall import ApiCall
import json

DOTABUFFURL = "https://www.dotabuff.com/matches/%d"
BROKEGAMES = [5036395844]
dotaApi = ApiCall()


# build an object for storing all of CDL
class CDL():
  seasons = []

  def __init__(self, leagueIds):
    for league in leagueIds:
      self.seasons.append(Season(league[1], league[0]))


# build an object for storing a single season
class Season():
  matches = []

  def __init__(self, seasonId, seasonNumber):
    resp = dotaApi.getLeague(league_id=seasonId)
    print("{0} matches parsing...".format(len(resp)))
    for index, match in enumerate(resp):
      if match not in BROKEGAMES:
        print('\r%d' % (index), end = '')
        match["seasonNumber"] = seasonNumber
        self.matches.append(Match(match['match_id']))

  def formatMatches(self):
    formattedMatches = []
    for match in self.matches:
      formattedMatches.append(match.__dict__)
    return formattedMatches


# build an object for storing a single match
class Match():

  def __init__(self, matchId):
    self.players = []
    self.matchId = matchId
    match = dotaApi.getMatch(match_id=self.matchId)
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
      performances.append(perf)
    return performances


# for testing purposes
if __name__ == "__main__":
  season = Season(10824, 1)