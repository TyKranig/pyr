CREATE_MATCH_TABLE = """
    create table if not exists
    Matches
    (match_id INTEGER, dire_team_id INTEGER, radiant_team_id INTEGER);
    """

CREATE_PLAYER_TABLE = """
    create table if not exists
    Players
    (
        match_id INTEGER, account_id INTEGER, name TEXT, kills INTEGER, deaths INTEGER,
        assists INTEGER, last_hits INTEGER, denies INTEGER, gold_per_min INTEGER, xp_per_min INTEGER
    );
"""

INSERT_MATCH = """
    INSERT INTO Matches VALUES
    (?, ?, ?)
"""

INSERT_PLAYER = """
    INSERT INTO Players VALUES
    (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""