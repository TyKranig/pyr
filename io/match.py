from apicall import ApiCall
import json

BROKEGAMES = [5036395844]
dotaApi = ApiCall()

class Season():
  matches = []

  def __init__(self, seasonId):
    resp = dotaApi.getLeague(league_id=seasonId)
    print("{0} matches parsing...".format(len(resp)))
    for index, match in enumerate(resp):
      if match not in BROKEGAMES:
        print('\r%d' % (index), end = '')
        self.matches.append(Match(match))

class Match():

  def __init__(self, match):
    self.matchId = match["match_id"]
    match = dotaApi.getMatch(match_id=self.matchId)
    for point in match:
      self.__setattr__(point, match[point])
    for player in self.players:
      realSteamId = player["account_id"] + 76561197960265728
      player["steamName"] = dotaApi.getPlayerName(steamids=realSteamId)

  def formatPerformances(self):
    performances = []
    for perf in self.players:
      perf["dotabuff"] = "https://www.dotabuff.com/matches/%d" % (self.matchId)
      perf["match_id"] = self.matchId
    return performances

if __name__ == "__main__":
  season = Season(10824)