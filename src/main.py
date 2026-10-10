import sqlite3
from pathlib import Path

directory = Path(__file__).parent.parent
path = directory / "database" / "schedule.db"
path = path.resolve()

conn = sqlite3.connect(path)
conn.close()
print("It works!")
print("Hello world!")