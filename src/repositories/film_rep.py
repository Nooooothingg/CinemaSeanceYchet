from database.database import get_conn
from src.models.film import Film

def _map(row) -> Film:
    return Film(*row)

def create(film_name: str, film_descr: str | None, film_time: int) -> None:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO Film (Film_name, Film_descr, Film_time) VALUES (?, ?, ?)",
        (film_name, film_descr, film_time)
    )
    conn.commit()
    conn.close()

def get_all() -> list[Film]:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT Film_ID, Film_name, Film_descr, Film_time FROM Film")
    rows = cur.fetchall()
    conn.close()
    return [_map(r) for r in rows]

def get_by_id(film_id: int) -> Film | None:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT Film_ID, Film_name, Film_time, Film_descr FROM Film WHERE Film_ID = ?", (film_id,))
    row = cur.fetchone()
    conn.close()
    return _map(row) if row else None

def update(film_id: int, film_name: str, film_descr: str | None, film_time: int) -> None:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "UPDATE Film SET Film_name = ?, Film_descr = ?, Film_time = ? WHERE Film_ID = ?",
        (film_name, film_descr, film_time, film_id)
    )
    conn.commit()
    conn.close()

def delete(film_id: int) -> None:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM Film WHERE Film_ID = ?", (film_id,))
    conn.commit()
    conn.close()