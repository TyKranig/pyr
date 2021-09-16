import requests
import json
import os
import datetime
from dotenv import load_dotenv


GETMATCHHISTORY = 'https://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/V001/?'
GETSINGLEMATCH = 'https://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/V001/?'
GETPLAYER = 'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?'


def get_key():
    load_dotenv()
    return os.environ['api_token']


class ApiCall:
    def __init__(self):
        self.key = get_key()
        self.session = requests.session()

    def getLeague(self, **kwargs):
        kwargs['key'] = self.key
        kwargs['tournament_games_only'] = 1
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
