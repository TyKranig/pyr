import sys, os
from cdlapi.dotaApi import ApiCall
import json
import pprint

# calls the api and outputs a "output.json" file containing match data
api = ApiCall()

resp = api.getLeague(league_id=11086)

out = open("output.json", "w")

print("{0} matches parsed...".format(len(resp['result']['matches'])))
# out.write(json.dumps(resp, indent=2, sort_keys=True))

for k in resp['result']['matches']:
    print(k["match_id"])

print(resp['result']['matches'][0]["match_id"])
out.write(json.dumps(api.getMatch(match_id=resp['result']['matches'][0]["match_id"]), indent=2))