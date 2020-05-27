#!/usr/bin/env python3
import json
import sqlite3
import datetime

from sheetwriter import SheetWriter
from apicall import ApiCall
import queries

SEASONS = [(1, 11359, "Season1"), (2, 10904, "Season2"),
           (3, 11590, "Season3"), (4, 11811, "Season4")]

DOTABUFF = "https://www.dotabuff.com/matches/{0}"

MATCH_COLS = [
    "match_id", "dire_team_id", "radiant_team_id", "season", "duration"
]

PLAYER_COLS = [
    "match_id", "account_id", "name", "kills", "deaths", "assists", "last_hits", "denies", 
    "gold_per_min", "xp_per_min", "season", "dotabuff"
]

def checkForMatch(cursor, match_id):
    for row in cursor.execute("Select match_id from Matches where match_id = ?", (match_id, )):
        return True
    return False

def loadData(cursor, seasonId, seasonNumber):
    dotaApi = ApiCall()
    resp = dotaApi.getLeague(league_id=seasonId)

    print("\n{0} matches parsing...".format(len(resp)))
 
    for index, match in enumerate(resp):
        print('\r%d' % (index), end = '')
        matchId = match['match_id']

        if not checkForMatch(cursor, matchId):
            response = dotaApi.getMatch(match_id=matchId)
            match["season"] = seasonNumber
            match["duration"] = str(datetime.timedelta(seconds=response["duration"]))

            data = tuple(match[col] for col in MATCH_COLS)
            cursor.execute(queries.INSERT_MATCH, data)

            for performance in response['players']:
                realSteamId = performance["account_id"] + 76561197960265728
                performance["name"] = dotaApi.getPlayerName(steamids=realSteamId)
                performance["season"] = seasonNumber
                performance["match_id"] = matchId
                performance["dotabuff"] = DOTABUFF.format(matchId)

                data = tuple(performance[col] for col in PLAYER_COLS)
                cursor.execute(queries.INSERT_PLAYER, data)

if __name__ == "__main__":
    conn = sqlite3.connect('games.db')
    cursor = conn.cursor()

    cursor.execute(queries.CREATE_MATCH_TABLE)
    cursor.execute(queries.CREATE_PLAYER_TABLE)

    for season in SEASONS:
        loadData(cursor, season[1], season[0])
        conn.commit()

        writer = SheetWriter(season[2])

        writer.writeArray("A2:C11", cursor.execute(queries.TOP_PLAYER_KILLS).fetchall())