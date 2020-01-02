import requests
import json
import os.path
import os
import datetime
from collections import namedtuple

GETMATCHHISTORY = 'https://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/V001/?'
GETSINGLEMATCH = 'https://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/V001/?'
GETPLAYER = 'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?'

def get_key():
    with open(os.getcwd() + r"/io/.env", "r") as file:
        key = file.read().strip()
    return key

class ApiCall:
  def __init__(self):
    self.key = get_key()
    self.session = requests.session()

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

  def getPlayerName(self, **kwargs):
    kwargs['key'] = self.key
    response = self.session.get(GETPLAYER, params=kwargs)
    return json.loads(response.text)['response']['players'][0]['personaname']

  def  _json_object_hook(d):
    return namedtuple('X', d.keys())(*d.values())
  
  def json2obj(data): 
    return json.loads(data, object_hook=_json_object_hook)
