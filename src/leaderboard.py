import duckdb
import os
from datetime import date

db = os.path.join(os.path.dirname(__file__), "leaderboard.duckdb")
_conn = duckdb.connect(db)

# creating table
_conn.execute("""
CREATE TABLE IF NOT EXISTS leaderboard (
    name VARCHAR,
    score INTEGER,
    date  DATE
)
""")

def add_score(name: str, score: int): # add date
    today = date.today().isoformat()
    _conn.execute("INSERT INTO leaderboard (name, score, date) VALUES (?, ?, ?)",
                  [name, score, today])
    
    # only keep top 10
only_top_scores = """
    DELETE FROM leaderboard
    WHERE score < (
    SELECT MIN(score) FROM (
    SELECT score FROM leaderboard
    ORDER BY score DESC
    LIMIT 10
    )
)              
"""
_conn.execute(only_top_scores)
    
# get top 10 scores
def get_entries() -> list[tuple]:
    query = """
      SELECT name, score, date
      FROM leaderboard
      ORDER BY score DESC, date DESC
      LIMIT 10
    """
    return _conn.execute(query).fetchall()