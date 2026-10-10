import sqlite3
from pathlib import Path

db_name = "schedule.db"

def get_conn():
    conn = sqlite3.connect(db_name)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():

    #if Path(db_name).exists():
    #    return
    conn = get_conn()

    sql_path = (Path(__file__).parent / "scheme.sql")

    with open(sql_path, 'r', encoding='utf-8') as file:
        sql_script = file.read()

    conn.executescript(sql_script)

    conn.commit()
    conn.close()

    print('Ну чего там?')
init_db()