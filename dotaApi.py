import requests
import json

def getLeague(id):
    key = "5E7240D91290A967CF6CADA6E9AB1502"

    response = requests.get(
            'https://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/V001/?key={0}&league_id={1}'
            .format(key, id))

    parsed = json.loads(response.text)
    return parsed