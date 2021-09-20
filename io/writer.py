#!/usr/bin/env python3
import json
import sqlite3
import datetime
import argparse

from sheetwriter import SheetWriter
from apicall import ApiCall
import queries

SEASONS_LOL = [
    (1, 10904, "Season0"),
    (2, 11359, "Season1"),
    (3, 11590, "Season2"),
    (4, 11811, "Season3"),
    (5, 12068, "Season4"),
    (6, 12300, "Season5"),
    (7, 12671, "Season6"),
    (8, 13177, "Season7"),
    (9, 13450, "Season8"),
]

SEASONS_MD2L = [
    (1, 12374, "Season7"),
    (2, 12691, "Season8")
]

SEASONS_RD2L_MASTERS = [
    (1, 12593, "Season1")
]

DBS = ["md2l.db", "lol.db", "rd2l.db"]

LEAGUES = {
    0 : SEASONS_MD2L,
    1 : SEASONS_LOL,
    2 : SEASONS_RD2L_MASTERS
}

CURRENT_LEAGUE = 0

DOTABUFF = "https://www.dotabuff.com/matches/{0}"

MATCH_COLS = [
    "match_id", "dire_team_id", "radiant_team_id", "season", "duration"
]

PLAYER_COLS = [
    "match_id", "account_id", "name", "kills", "deaths", "assists", "last_hits", "denies", 
    "gold_per_min", "xp_per_min", "season", "dotabuff"
]

SKIPPED_MATCHES = []

def checkForMatch(cursor, match_id):
    for row in cursor.execute("Select match_id from Matches where match_id = ?", (match_id, )):
        return True
    if match_id in SKIPPED_MATCHES:
        print(match_id)
        return True
    return False

def loadSkipMatches():
    with open("skipGames") as file:
        lines = file.readlines()
        lines = [int(line.rstrip()) for line in lines]
        return lines

def loadData(cursor, seasonId, seasonNumber):
    dotaApi = ApiCall()
    lastMatch = 1

    while(lastMatch > 0):
        if(lastMatch == 1):
            # first time through use no last match id
            resp = dotaApi.getLeague(league_id=seasonId)
        else:
            # second time we hit the max so start over
            resp = dotaApi.getLeague(league_id=seasonId, start_at_match_id=lastMatch)
        print("\n{0} matches parsing...".format(len(resp)))
        lastMatch = insertMatches(cursor, seasonId, seasonNumber, dotaApi, resp)

def insertMatches(cursor, seasonId, seasonNumber, dotaApi, data):
    last = -1
    for index, match in enumerate(data):
        print('\r%d' % (index), end="", flush=True)
        matchId = match['match_id']

        # set the flag if we reach match max
        if(index == 126):
            print("got 127 doing more")
            last = matchId

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
    return last

if __name__ == "__main__":
    SKIPPED_MATCHES = loadSkipMatches()
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument("league", type=int)
    args = parser.parse_args()

    conn = sqlite3.connect(DBS[args.league])
    cursor = conn.cursor()

    cursor.execute(queries.CREATE_MATCH_TABLE)
    cursor.execute(queries.CREATE_PLAYER_TABLE)

    for season in LEAGUES[args.league]:
        print(season[1], season[0])
        loadData(cursor, season[1], season[0])
        conn.commit()

        writer = SheetWriter(season[2], args.league)

        writer.writeArray("A2:C11", cursor.execute(queries.TOP_PLAYER_KILLS_SEASON, (season[0], )).fetchall())
        writer.writeArray("E2:G11", cursor.execute(queries.TOP_PLAYER_KILLS_TOTAL_SEASON, (season[0], )).fetchall())
        writer.writeArray("I2:K11", cursor.execute(queries.TOP_PLAYER_KILLS_AVG_SEASON, (season[0], )).fetchall())

        writer.writeArray("A14:C23", cursor.execute(queries.TOP_PLAYER_DEATHS_SEASON, (season[0], )).fetchall())
        writer.writeArray("E14:G23", cursor.execute(queries.TOP_PLAYER_DEATHS_TOTAL_SEASON, (season[0], )).fetchall())
        writer.writeArray("I14:K23", cursor.execute(queries.TOP_PLAYER_DEATHS_AVG_SEASON, (season[0], )).fetchall())
        writer.writeArray("L14:N23", cursor.execute(queries.LOW_PLAYER_DEATHS_AVG_SEASON, (season[0], )).fetchall())
        writer.writeArray("O14:Q23", cursor.execute(queries.LOW_PLAYER_DEATHS_season, (season[0], )).fetchall())

        writer.writeArray("A26:C35", cursor.execute(queries.TOP_PLAYER_ASSISTS_SEASON, (season[0], )).fetchall())
        writer.writeArray("E26:G35", cursor.execute(queries.TOP_PLAYER_ASSISTS_TOTAL_SEASON, (season[0], )).fetchall())
        writer.writeArray("I26:K35", cursor.execute(queries.TOP_PLAYER_ASSISTS_AVG_SEASON, (season[0], )).fetchall())

        writer.writeArray("A38:C47", cursor.execute(queries.TOP_PLAYER_CS_GAME_SEASON, (season[0], )).fetchall())
        writer.writeArray("E38:G47", cursor.execute(queries.TOP_PLAYER_CS_TOTAL_SEASON, (season[0], )).fetchall())
        writer.writeArray("I38:K47", cursor.execute(queries.TOP_PLAYER_CS_AVG_SEASON, (season[0], )).fetchall())

        writer.writeArray("A50:C59", cursor.execute(queries.TOP_PLAYER_GPM_GAME_SEASON, (season[0], )).fetchall())
        writer.writeArray("I50:K59", cursor.execute(queries.TOP_PLAYER_GPM_AVG_SEASON, (season[0], )).fetchall())

        writer.writeArray("A62:C71", cursor.execute(queries.TOP_PLAYER_XPM_GAME_SEASON, (season[0], )).fetchall())
        writer.writeArray("E62:G71", cursor.execute(queries.TOP_PLAYER_XPM_AVG_SEASON, (season[0], )).fetchall())


    writer = SheetWriter("AllTime", args.league)
    writer.writeArray("A2:C11", cursor.execute(queries.TOP_PLAYER_KILLS_ALLTIME).fetchall())
    writer.writeArray("E2:G11", cursor.execute(queries.TOP_PLAYER_KILLS_TOTAL_ALLTIME).fetchall())
    writer.writeArray("I2:K11", cursor.execute(queries.TOP_PLAYER_KILLS_AVG_ALLTIME).fetchall())

    writer.writeArray("A14:C23", cursor.execute(queries.TOP_PLAYER_DEATHS_ALLTIME).fetchall())
    writer.writeArray("E14:G23", cursor.execute(queries.TOP_PLAYER_DEATHS_TOTAL_ALLTIME).fetchall())
    writer.writeArray("I14:K23", cursor.execute(queries.TOP_PLAYER_DEATHS_AVG_ALLTIME).fetchall())
    writer.writeArray("L14:N23", cursor.execute(queries.LOW_PLAYER_DEATHS_AVG_ALLTIME).fetchall())
    writer.writeArray("O14:Q23", cursor.execute(queries.LOW_PLAYER_DEATHS_alltime).fetchall())

    writer.writeArray("A26:C35", cursor.execute(queries.TOP_PLAYER_ASSISTS_ALLTIME).fetchall())
    writer.writeArray("E26:G35", cursor.execute(queries.TOP_PLAYER_ASSISTS_TOTAL_ALLTIME).fetchall())
    writer.writeArray("I26:K35", cursor.execute(queries.TOP_PLAYER_ASSISTS_AVG_ALLTIME).fetchall())

    writer.writeArray("A38:C47", cursor.execute(queries.TOP_PLAYER_CS_GAME_ALLTIME).fetchall())
    writer.writeArray("E38:G47", cursor.execute(queries.TOP_PLAYER_CS_TOTAL_ALLTIME).fetchall())
    writer.writeArray("I38:K47", cursor.execute(queries.TOP_PLAYER_CS_AVG_ALLTIME).fetchall())

    writer.writeArray("A50:C59", cursor.execute(queries.TOP_PLAYER_GPM_GAME_ALLTIME).fetchall())
    writer.writeArray("I50:K59", cursor.execute(queries.TOP_PLAYER_GPM_AVG_ALLTIME).fetchall())

    writer.writeArray("A62:C71", cursor.execute(queries.TOP_PLAYER_XPM_GAME_ALLTIME).fetchall())
    writer.writeArray("E62:G71", cursor.execute(queries.TOP_PLAYER_XPM_AVG_ALLTIME).fetchall())