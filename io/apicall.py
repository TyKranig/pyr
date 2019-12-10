import requests
import json
import os.path
from endpoints import GETMATCHHISTORY, GETSINGLEMATCH, GETPLAYER

def get_key():
    with open(".env", "r") as file:
        key = file.read().strip()
    return key

class ApiCall:
    key = get_key()

    def getLeague(self, session, **kwargs):
        kwargs['key'] = self.key
        response = requests.get(GETMATCHHISTORY, params=kwargs)
        return json.loads(response.text)

    def getMatch(self, session, **kwargs):
        kwargs['key'] = self.key
        response = session.get(GETSINGLEMATCH, params=kwargs)
        return json.loads(response.text)

    def getPlayerSummary(self, session, **kwargs):
        kwargs['key'] = self.key
        response = session.get(GETPLAYER, params=kwargs)
        return json.loads(response.text)["response"]["players"][0]