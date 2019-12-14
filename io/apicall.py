import requests
import json
import os.path

GETMATCHHISTORY = 'https://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/V001/?'
GETSINGLEMATCH = 'https://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/V001/?'
GETPLAYER = 'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?'

def get_key():
    with open(".env", "r") as file:
        key = file.read().strip()
    return key

class ApiCall:
    key = get_key()
    self.session = requests.session()

    def getLeague(self, **kwargs):
        kwargs['key'] = self.key
        response = self.requests.get(GETMATCHHISTORY, params=kwargs)
        return json.loads(response.text)

    def getMatch(self, **kwargs):
        kwargs['key'] = self.key
        response = self.session.get(GETSINGLEMATCH, params=kwargs)
        return json.loads(response.text)

    def getPlayerSummary(self, **kwargs):
        kwargs['key'] = self.key
        response = self.session.get(GETPLAYER, params=kwargs)
        return json.loads(response.text)["response"]["players"][0]