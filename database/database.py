import sqlite3
from pathlib import Path

db_path = Path(__file__).parent / "schedule.db"

def get_conn():
    conn = sqlite3.connect(str(db_path))
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    conn = get_conn()

    sql_path = Path(__file__).parent / "scheme.sql"

    with open(sql_path, 'r', encoding='utf-8') as file:
        sql_script = file.read()

    conn.executescript(sql_script)

    conn.commit()
    conn.close()

init_db()