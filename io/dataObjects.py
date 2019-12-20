from apicall import ApiCall
import json

DOTABUFFURL = "https://www.dotabuff.com/matches/%d"
BROKEGAMES = [5036395844]
dotaApi = ApiCall()

class CDL():
  seasons = []

  def __init__(self, leagueIds):
    for league in leagueIds:
      self.seasons.append(Season(leagueIds[1]))

class Season():
  matches = []

  def __init__(self, seasonId):
    resp = dotaApi.getLeague(league_id=seasonId)
    print("{0} matches parsing...".format(len(resp)))
    for index, match in enumerate(resp):
      if match not in BROKEGAMES:
        print('\r%d' % (index), end = '')
        self.matches.append(Match(match['match_id']))

class Match():

  def __init__(self, matchId):
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

if __name__ == "__main__":
  season = Season(10824)