import requests
import json
import endpoints
from key import get_key

class ApiCall:
    
    key = get_key()

    def getLeague(self, **kwargs):
        kwargs['key'] = self.key

        response = requests.get(
                endpoints.GETMATCHHISTORY,
                params=kwargs
        )
        return json.loads(response.text)

    def getMatch(self, **kwargs):
        kwargs['key'] = self.key

        response = requests.get(
                endpoints.GETSINGLEMATCH,
                params=kwargs
        )
        return json.loads(response.text)