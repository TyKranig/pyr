from apicall import ApiCall
import json

class Season():
  matches = []

  def __init__(self):
    self.match = Match(13456)

class Match():
  dotaApi = ApiCall()

  def __init__(self, matchId):
    match = self.dotaApi.getMatch(match_id=matchId)
    for point in match:
      self.__setattr__(point, match[point])
    


if __name__ == "__main__":
    match = Match(4746735792)