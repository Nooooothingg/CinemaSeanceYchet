from database.database import get_conn
from src.models.user_role import UserRole

def _map(row) -> UserRole:
    return UserRole(*row)

def create(role_name: str, description: str | None) -> None:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO UserRole (role_name, description) VALUES (?, ?)",
        (role_name, description)
    )
    conn.commit()
    conn.close()

def get_all() -> list[UserRole]:
    conn = get_conn()
    cur = conn.cursor()
    # Обратите внимание: в БД колонка может называться Role_ID или UserRole_ID.
    # Я использую Role_ID, но если в вашей БД иначе - поменяйте в SQL.
    cur.execute("SELECT Role_ID, role_name, description FROM UserRole")
    rows = cur.fetchall()
    conn.close()
    return [_map(r) for r in rows]

def get_by_id(role_id: int) -> UserRole | None:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT Role_ID, role_name, description FROM UserRole WHERE Role_ID = ?", (role_id,))
    row = cur.fetchone()
    conn.close()
    return _map(row) if row else None