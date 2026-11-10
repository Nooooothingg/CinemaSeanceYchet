from src.database.database import get_conn
from src.models.cinema import Cinema

def _map(row) -> Cinema:
    return Cinema(*row)

def create(cinemaname: str, description: str | None, link: str | None) -> None:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO Cinema (name, description, link) VALUES (?, ?, ?)",
        (cinemaname, description, link)
    )
    conn.commit()
    conn.close()

def get_all() -> list[Cinema]:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT Cinema_ID, name, description, link FROM Cinema")
    rows = cur.fetchall()
    conn.close()
    return [_map(r) for r in rows]

def get_by_id(cinema_id: int) -> Cinema | None:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT Cinema_ID, name, description, link FROM Cinema WHERE Cinema_ID = ?", (cinema_id,))
    row = cur.fetchone()
    conn.close()
    return _map(row) if row else None