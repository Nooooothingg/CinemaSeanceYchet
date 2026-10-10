import sqlite3
from pathlib import Path
conn = sqlite3.connect("schedule.db")
conn.close()
print("It works!")
print("Hello world!")