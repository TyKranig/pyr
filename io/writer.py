import sys, os
print(os.path.join(os.path.realpath(__file__)))
sys.path.append(os.path.join(os.path.dirname(__file__), "../api/"))
from api.dotaApi import ApiCall
import json

api = ApiCall()

resp = api.getLeague(league_id=11086)

out = open("output.json", "w")

print("{0} matches parsed...".format(len(resp['result']['matches'])))
out.write(json.dumps(resp, indent=2, sort_keys=True))

for k in resp['result']['matches']:
    print(k["match_id"])

# print(api.getMatch(match_id=))