#!/usr/bin/env python3
import json
import sqlite3

from sheetwriter import SheetWriter
from apicall import ApiCall
import queries

SEASONS = [(1, 10824, "Season1"), (2, 11086, "Season2"),
           (3, 11336, "Season3"), (4, 11560, "Season4")]

PLAYER_COLS = [
    "match_id", "account_id", "kills", "deaths", "assists", "last_hits", "denies", 
    "gold_per_min", "xp_per_min"
]

def setupDatabase():
    conn = sqlite3.connect('games.db')
    c = conn.cursor()
    c.execute(queries.CREATE_MATCH_TABLE)
    c.execute(queries.CREATE_PLAYER_TABLE)
    return c

if __name__ == "__main__":
    dotaApi = ApiCall()
    resp = dotaApi.getLeague(league_id=10824)
    # print(json.dumps(resp, indent=4, sort_keys=True))

    cursor = setupDatabase()

    for match in resp:
        matchId = match['match_id']
        response = dotaApi.getMatch(match_id=matchId)

        data = (
            match['match_id'], 
            match['dire_team_id'], 
            match['radiant_team_id']
        )

        cursor.execute(queries.INSERT_MATCH, data)

        for performance in response['players']:
            print(performance)
            data = (
                performance['account_id'],
                performance['kills']
            )

        break

    cursor.execute("select * from Matches")
    print(cursor.fetchone())