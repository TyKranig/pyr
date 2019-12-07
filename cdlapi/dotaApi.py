import requests
import json
from cdlapi import endpoints
from cdlapi import get_key

class ApiCall:
    key = get_key()

    def getLeague(self, session, **kwargs):
        kwargs['key'] = self.key
        response = requests.get(endpoints.GETMATCHHISTORY, params=kwargs)
        return json.loads(response.text)

    def getMatch(self, session, **kwargs):
        kwargs['key'] = self.key
        response = session.get(endpoints.GETSINGLEMATCH, params=kwargs)
        return json.loads(response.text)

    def getPlayerSummary(self, session, **kwargs):
        kwargs['key'] = self.key
        response = session.get(endpoints.GETPLAYER, params=kwargs)
        return json.loads(response.text)["response"]["players"][0]