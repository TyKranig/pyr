from dotaApi import getLeague
import json

resp = getLeague(11086)

out = open("output.json", "w")
print(len(resp['result']['matches']))
out.write(json.dumps(resp, indent=2, sort_keys=True))   