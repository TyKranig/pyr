import requests
import json
import os.path
import datetime

GETMATCHHISTORY = 'https://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/V001/?'
GETSINGLEMATCH = 'https://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/V001/?'
GETPLAYER = 'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?'

def get_key():
    with open("io\.env", "r") as file:
        key = file.read().strip()
    return key

class ApiCall:
  def __init__(self):
    self.key = get_key()
    self.session = requests.session()
  # TODO potentially use an object instead to store matches in order to get repsonse cleaner
  # Match object would store matches to skip, leagues, and match ids to add
  def getLeague(self, **kwargs):
    kwargs['key'] = self.key
    response = self.session.get(GETMATCHHISTORY, params=kwargs)
    return json.loads(response.text)['result']['matches']

  def getMatch(self, **kwargs):
    kwargs['key'] = self.key
    response = self.session.get(GETSINGLEMATCH, params=kwargs)
    match = json.loads(response.text)['result']
    match["string_duration"] = str(datetime.timedelta(seconds=match["duration"]))
    match["dotabuff"] = "https://www.dotabuff.com/matches/{0}".format(kwargs["match_id"])
    return match

  def getPlayerSummary(self, performance, match_id):
    # Steam api only lets you look up players with a 64bit account id, the one stored in dota is 32bit
    sixtyfour = performance["account_id"] + 76561197960265728
    response = self.session.get(GETPLAYER, key=self.key, steamids=sixtyfour)["personaname"]
    performance["player_name"] = json.loads(response.text)["response"]["players"][0]["personaname"]
    performance["dotabuff"] = "https://www.dotabuff.com/matches/{0}".format(match_id)
    performance["match_id"] = match_id
    return performance

  def getMatchJson(self, **kwargs):
    match = self.getMatch(kwargs)
    players = []
    for player in match["players"]:
      players.append(self.getPlayerSummary(player, match["match_id"]))
    return (match, players)