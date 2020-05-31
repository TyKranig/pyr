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




TOP_PLAYER_KILLS_SEASON = """
    select kills, name, dotabuff from Players 
    where season = ? order by kills desc limit 10
"""



TOP_PLAYER_KILLS_ALLTIME = """
    select kills, name, dotabuff from Players 
    order by kills desc limit 10
"""

TOP_PLAYER_DEATHS_SEASON = """
    select deaths, name, dotabuff from Players 
    where season = ? order by deaths desc limit 10
"""

TOP_PLAYER_DEATHS_ALLTIME = """
    select deaths, name, dotabuff from Players 
    order by deaths desc limit 10
"""

TOP_PLAYER_DEATHS_SEASON = """
    select deaths, name, dotabuff from Players 
    where season = ? order by deaths desc limit 10
"""

TOP_PLAYER_DEATHS_ALLTIME = """
    select deaths, name, dotabuff from Players 
    order by deaths desc limit 10
"""

TOP_PLAYER_ASSISTS_SEASON = """
    select assists, name, dotabuff from Players 
    where season = ? order by assists desc limit 10
"""

TOP_PLAYER_ASSISTS_ALLTIME = """
    select assists, name, dotabuff from Players 
    order by assists desc limit 10
"""

TOP_PLAYER_CS_GAME_SEASON = """
    select last_hits, name, dotabuff from Players 
    where season = ? order by last_hits desc limit 10
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