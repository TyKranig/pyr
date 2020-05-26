CREATE_MATCH_TABLE = """
    create table if not exists
    Matches
    (match_id INTEGER, dire INTEGER, radiant INTEGER);
    """

CREATE_PLAYER_TABLE = """
    create table if not exists
    Players
    (player_id INTEGER, kills int);
"""

INSERT_MATCH = """
    INSERT INTO Matches VALUES
    (?, ?, ?)
"""

INSERT_PLAYER = """
    INSERT INTO Players VALUES
    (?, ?)
"""