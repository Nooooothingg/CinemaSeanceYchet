from database.database import get_conn
from src.models.user import User

def _map(row) -> User:
    return User(*row)

def create(userrole_id: int, username: str, login: str, passwordhash: str) -> None:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO Users (UserRole_ID, username, login, passwordHash) VALUES (?, ?, ?, ?)",
        (userrole_id, username, login, passwordhash)
    )
    conn.commit()
    conn.close()

def get_by_login(login: str) -> User | None:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "SELECT User_ID, UserRole_ID, username, login, passwordHash FROM Users WHERE login = ?",
        (login,)
    )
    row = cur.fetchone()
    conn.close()
    return _map(row) if row else None

def get_all() -> list[User]:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT User_ID, UserRole_ID, username, login, passwordHash FROM Users")
    rows = cur.fetchall()
    conn.close()
    return [_map(r) for r in rows]

def update(user_id: int, userrole_id: int, username: str, login: str, passwordhash: str) -> None:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "UPDATE Users SET UserRole_ID = ?, username = ?, login = ?, passwordHash = ? WHERE User_ID = ?",
        (userrole_id, username, login, passwordhash, user_id)
    )
    conn.commit()
    conn.close()

def delete(user_id: int) -> None:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM Users WHERE User_ID = ?", (user_id,))
    conn.commit()
    conn.close()