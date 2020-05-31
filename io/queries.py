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
    order by kills desc limit 10
"""

TOP_PLAYER_KILLS_TOTAL_SEASON = """
    select sum(kills) total_kills, name, dotabuff from Players
    where season = ?
    group by account_id
    order by total_kills desc limit 10
"""

TOP_PLAYER_KILLS_TOTAL_ALLTIME = """
    select sum(kills) total_kills, name, dotabuff from Players
    group by account_id
    order by total_kills desc limit 10
"""

TOP_PLAYER_KILLS_AVG_SEASON = """
    select avg(kills) avg_kills, name, dotabuff from Players
    where season = ?
    group by account_id
    order by avg_kills desc limit 10
"""

TOP_PLAYER_KILLS_AVG_ALLTIME = """
    select avg(kills) avg_kills, name, dotabuff from Players
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
    order by deaths desc limit 10
"""

TOP_PLAYER_DEATHS_TOTAL_SEASON = """
    select sum(deaths) total_deaths, name, dotabuff from Players
    where season = ?
    group by account_id
    order by total_deaths desc limit 10
"""

TOP_PLAYER_DEATHS_TOTAL_ALLTIME = """
    select sum(deaths) total_deaths, name, dotabuff from Players
    group by account_id
    order by total_deaths desc limit 10
"""

TOP_PLAYER_DEATHS_AVG_SEASON = """
    select avg(deaths) avg_deaths, name, dotabuff from Players
    where season = ?
    group by account_id
    order by avg_deaths desc limit 10
"""

TOP_PLAYER_DEATHS_AVG_ALLTIME = """
    select avg(deaths) avg_deaths, name, dotabuff from Players
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
    order by assists desc limit 10
"""

TOP_PLAYER_ASSISTS_TOTAL_SEASON = """
    select sum(assists) total_assists, name, dotabuff from Players
    where season = ?
    group by account_id
    order by total_assists desc limit 10
"""

TOP_PLAYER_ASSISTS_TOTAL_ALLTIME = """
    select sum(assists) total_assists, name, dotabuff from Players
    group by account_id
    order by total_assists desc limit 10
"""

TOP_PLAYER_ASSISTS_AVG_SEASON = """
    select avg(assists) avg_assists, name, dotabuff from Players
    where season = ?
    group by account_id
    order by avg_assists desc limit 10
"""

TOP_PLAYER_ASSISTS_AVG_ALLTIME = """
    select avg(assists) avg_assists, name, dotabuff from Players
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
    order by last_hits desc limit 10
"""

TOP_PLAYER_CS_TOTAL_SEASON = """
    select sum(last_hits) total_cs, name, dotabuff from Players
    where season = ?
    group by account_id
    order by total_cs desc limit 10
"""

TOP_PLAYER_CS_TOTAL_ALLTIME = """
    select sum(last_hits) total_cs, name, dotabuff from Players
    group by account_id
    order by total_cs desc limit 10
"""

TOP_PLAYER_CS_AVG_SEASON = """
    select avg(last_hits) avg_cs, name, dotabuff from Players
    where season = ?
    group by account_id
    order by avg_cs desc limit 10
"""

TOP_PLAYER_CS_AVG_ALLTIME = """
    select avg(last_hits) avg_cs, name, dotabuff from Players
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
    order by gold_per_min desc limit 10
"""

TOP_PLAYER_GPM_TOTAL_SEASON = """
    select sum(gold_per_min) total_gpm, name, dotabuff from Players
    where season = ?
    group by account_id
    order by total_gpm desc limit 10
"""

TOP_PLAYER_GPM_TOTAL_ALLTIME = """
    select sum(gold_per_min) total_gpm, name, dotabuff from Players
    group by account_id
    order by total_gpm desc limit 10
"""

TOP_PLAYER_GPM_AVG_SEASON = """
    select avg(gold_per_min) avg_gpm, name, dotabuff from Players
    where season = ?
    group by account_id
    order by avg_gpm desc limit 10
"""

TOP_PLAYER_GPM_AVG_ALLTIME = """
    select avg(gold_per_min) avg_gpm, name, dotabuff from Players
    group by account_id
    order by avg_gpm desc limit 10
"""