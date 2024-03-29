CREATE_MATCH_TABLE = """
    create table if not exists
    Matches
    (
        match_id INTEGER, dire_team_id INTEGER, radiant_team_id INTEGER,
        season INTEGER, duration TEXT
    );
    """

CREATE_PLAYER_TABLE = """
    create table if not exists
    Players
    (
        match_id INTEGER, account_id INTEGER, name TEXT, kills INTEGER, deaths INTEGER,
        assists INTEGER, last_hits INTEGER, denies INTEGER, gold_per_min INTEGER, xp_per_min INTEGER,
        season INTEGER, dotabuff TEXT
    );
"""

INSERT_MATCH = """
    INSERT INTO Matches VALUES
    (?, ?, ?, ?, ?)
"""

INSERT_PLAYER = """
    INSERT INTO Players VALUES
    (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""



# KILLS
TOP_PLAYER_KILLS_SEASON = """
    select kills, name, dotabuff from Players 
    where season = ? 
    order by kills desc limit 10
"""

TOP_PLAYER_KILLS_ALLTIME = """
    select kills, name, dotabuff from Players
    where season != 0
    order by kills desc limit 10
"""

TOP_PLAYER_KILLS_TOTAL_SEASON = """
    select sum(kills) total_kills, name, '' from Players
    where season = ?
    group by account_id
    order by total_kills desc limit 10
"""

TOP_PLAYER_KILLS_TOTAL_ALLTIME = """
    select sum(kills) total_kills, name, '' from Players
    where season != 0
    group by account_id
    order by total_kills desc limit 10
"""

TOP_PLAYER_KILLS_AVG_SEASON = """
    select ROUND(avg(kills),2) avg_kills, name, '' from Players
    where season = ?
    group by account_id
    order by avg_kills desc limit 10
"""

TOP_PLAYER_KILLS_AVG_ALLTIME = """
    select  ROUND(avg(kills),2) avg_kills, name, '' from Players
    where season != 0
    group by account_id
    order by avg_kills desc limit 10
"""


# DEATHS
TOP_PLAYER_DEATHS_SEASON = """
    select deaths, name, dotabuff from Players 
    where season = ? order by deaths desc limit 10
"""

TOP_PLAYER_DEATHS_ALLTIME = """
    select deaths, name, dotabuff from Players
    where season != 0
    order by deaths desc limit 10
"""

TOP_PLAYER_DEATHS_TOTAL_SEASON = """
    select sum(deaths) total_deaths, name, '' from Players
    where season = ?
    group by account_id
    order by total_deaths desc limit 10
"""

TOP_PLAYER_DEATHS_TOTAL_ALLTIME = """
    select sum(deaths) total_deaths, name, '' from Players
    where season != 0
    group by account_id
    order by total_deaths desc limit 10
"""

TOP_PLAYER_DEATHS_AVG_SEASON = """
    select ROUND(avg(deaths),2) avg_deaths, name, '' from Players
    where season = ?
    group by account_id
    order by avg_deaths desc limit 10
"""

LOW_PLAYER_DEATHS_AVG_SEASON = """
    select ROUND(avg(deaths),2) avg_deaths, name, '' from Players
    where season = ?
    group by account_id
    order by avg_deaths asc limit 10
"""
LOW_PLAYER_DEATHS_AVG_ALLTIME = """
    select ROUND(avg(deaths),2) avg_deaths, name, '' from Players
    group by account_id
    order by avg_deaths asc limit 10
"""
LOW_PLAYER_DEATHS_season = """
    select sum(deaths) avg_deaths, name, '' from Players
    where season = ?
    group by account_id
    order by avg_deaths asc limit 10
"""
LOW_PLAYER_DEATHS_alltime = """
    select sum(deaths) avg_deaths, name, '' from Players
    group by account_id
    order by avg_deaths asc limit 10
"""

TOP_PLAYER_DEATHS_AVG_ALLTIME = """
    select ROUND(avg(deaths),2) avg_deaths, name, '' from Players
    where season != 0
    group by account_id
    order by avg_deaths desc limit 10
"""


# ASSISTS
TOP_PLAYER_ASSISTS_SEASON = """
    select assists, name, dotabuff from Players
    where season = ?
    order by assists desc limit 10
"""

TOP_PLAYER_ASSISTS_ALLTIME = """
    select assists, name, dotabuff from Players
    where season != 0
    order by assists desc limit 10
"""

TOP_PLAYER_ASSISTS_TOTAL_SEASON = """
    select sum(assists) total_assists, name, '' from Players
    where season = ?
    group by account_id
    order by total_assists desc limit 10
"""

TOP_PLAYER_ASSISTS_TOTAL_ALLTIME = """
    select sum(assists) total_assists, name, '' from Players
    where season != 0
    group by account_id
    order by total_assists desc limit 10
"""

TOP_PLAYER_ASSISTS_AVG_SEASON = """
    select ROUND(avg(assists),2) avg_assists, name, '' from Players
    where season = ?
    group by account_id
    order by avg_assists desc limit 10
"""

TOP_PLAYER_ASSISTS_AVG_ALLTIME = """
    select ROUND(avg(assists),2) avg_assists, name, '' from Players
    where season != 0
    group by account_id
    order by avg_assists desc limit 10
"""

# LAST HITS
TOP_PLAYER_CS_GAME_SEASON = """
    select last_hits, name, dotabuff from Players 
    where season = ? 
    order by last_hits desc limit 10
"""

TOP_PLAYER_CS_GAME_ALLTIME = """
    select last_hits, name, dotabuff from Players
    where season != 0
    order by last_hits desc limit 10
"""

TOP_PLAYER_CS_TOTAL_SEASON = """
    select sum(last_hits) total_cs, name, '' from Players
    where season = ?
    group by account_id
    order by total_cs desc limit 10
"""

TOP_PLAYER_CS_TOTAL_ALLTIME = """
    select sum(last_hits) total_cs, name, '' from Players
    where season != 0
    group by account_id
    order by total_cs desc limit 10
"""

TOP_PLAYER_CS_AVG_SEASON = """
    select ROUND(avg(last_hits),2) avg_cs, name, '' from Players
    where season = ?
    group by account_id
    order by avg_cs desc limit 10
"""

TOP_PLAYER_CS_AVG_ALLTIME = """
    select ROUND(avg(last_hits),2) avg_cs, name, '' from Players
    where season != 0
    group by account_id
    order by avg_cs desc limit 10
"""


# Gold Per Min
TOP_PLAYER_GPM_GAME_SEASON = """
    select gold_per_min, name, dotabuff from Players 
    where season = ?
    order by gold_per_min desc limit 10
"""

TOP_PLAYER_GPM_GAME_ALLTIME = """
    select gold_per_min, name, dotabuff from Players
    where season != 0
    order by gold_per_min desc limit 10
"""

TOP_PLAYER_GPM_AVG_SEASON = """
    select ROUND(avg(gold_per_min),2) avg_gpm, name, '' from Players
    where season = ?
    group by account_id
    order by avg_gpm desc limit 10
"""

TOP_PLAYER_GPM_AVG_ALLTIME = """
    select ROUND(avg(gold_per_min),2) avg_gpm, name, '' from Players
    where season != 0
    group by account_id
    order by avg_gpm desc limit 10
"""


# XPM
TOP_PLAYER_XPM_GAME_SEASON = """
    select xp_per_min, name, dotabuff from Players 
    where season = ?
    order by xp_per_min desc limit 10
"""

TOP_PLAYER_XPM_AVG_SEASON = """
    select ROUND(avg(xp_per_min),2) avg_xp, name, '' from Players
    where season = ?
    group by account_id
    order by avg_xp desc limit 10
"""

TOP_PLAYER_XPM_GAME_ALLTIME = """
    select xp_per_min, name, dotabuff from Players
    where season != 0
    order by xp_per_min desc limit 10
"""

TOP_PLAYER_XPM_AVG_ALLTIME = """
    select ROUND(avg(xp_per_min),2) avg_xpm, name, '' from Players
    where season != 0
    group by account_id
    order by avg_xpm desc limit 10
"""