#!/usr/bin/env python3
import json
import sqlite3

from sheetwriter import SheetWriter
from apicall import ApiCall
import queries

SEASONS = [(1, 11359, "Season1"), (2, 10904, "Season2"),
           (3, 11590, "Season3"), (4, 11811, "Season4")]

MATCH_COLS = [
    "match_id", "dire_team_id", "radiant_team_id"
]

PLAYER_COLS = [
    "match_id", "account_id", "name", "kills", "deaths", "assists", "last_hits", "denies", 
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

    cursor = setupDatabase()
 
    for match in resp:
        matchId = match['match_id']
        response = dotaApi.getMatch(match_id=matchId)

        data = tuple(match[col] for col in MATCH_COLS)
        cursor.execute(queries.INSERT_MATCH, data)

        for performance in response['players']:
            realSteamId = performance["account_id"] + 76561197960265728
            performance["name"] = dotaApi.getPlayerName(steamids=realSteamId)
            performance["match_id"] = matchId

            data = tuple(performance[col] for col in PLAYER_COLS)
            cursor.execute(queries.INSERT_PLAYER, data)

        break

    cursor.execute("select name, kills from Players order by kills desc")
    print(cursor.fetchall())