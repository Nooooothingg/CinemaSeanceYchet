from database.database import get_conn
from src.models.schedule import Schedule
import datetime


def _map(row) -> Schedule:
    # Вручную распределяем поля, так как тут используется JOIN
    # row[0] = Schedule_ID, row[1] = date_time, row[2] = Film_ID, row[3] = Cinema_ID, row[4] = admin_id
    # row[5] = film_name (из таблицы Film), row[6] = cinema_name (из таблицы Cinema)

    # Если из БД дата приходит как строка, ее можно сконвертировать в datetime:
    # dt = datetime.datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S') if isinstance(row[1], str) else row[1]

    return Schedule(
        schedule_id=row[0],
        date_time=row[1],
        film_id=row[2],
        cinema_id=row[3],
        admin_id=row[4],
        film_name=row[5],
        cinema_name=row[6]
    )


def create(date_time: datetime.datetime, film_id: int, cinema_id: int, admin_id: int) -> None:
    conn = get_conn()
    cur = conn.cursor()
    # Преобразуем datetime в строку для SQLite
    dt_str = date_time.strftime('%Y-%m-%d %H:%M:%S')
    cur.execute(
        "INSERT INTO Schedule (date_time, Film_ID, Cinema_ID, admin_id) VALUES (?, ?, ?, ?)",
        (dt_str, film_id, cinema_id, admin_id)
    )
    conn.commit()
    conn.close()


def get_all() -> list[Schedule]:
    conn = get_conn()
    cur = conn.cursor()
    # Делаем JOIN, чтобы получить имена фильма и кинотеатра
    cur.execute("""
        SELECT 
            s.Schedule_ID, s.date_time, s.Film_ID, s.Cinema_ID, s.admin_id,
            f.film_name, c.name
        FROM Schedule s
        JOIN Film f ON s.Film_ID = f.Film_ID
        JOIN Cinema c ON s.Cinema_ID = c.Cinema_ID
        ORDER BY s.date_time DESC
    """)
    rows = cur.fetchall()
    conn.close()
    return [_map(r) for r in rows]


def get_by_id(schedule_id: int) -> Schedule | None:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT 
            s.Schedule_ID, s.date_time, s.Film_ID, s.Cinema_ID, s.admin_id,
            f.film_name, c.name
        FROM Schedule s
        JOIN Film f ON s.Film_ID = f.Film_ID
        JOIN Cinema c ON s.Cinema_ID = c.Cinema_ID
        WHERE s.Schedule_ID = ?
    """, (schedule_id,))
    row = cur.fetchone()
    conn.close()
    return _map(row) if row else None


def update(schedule_id: int, date_time: datetime.datetime, film_id: int, cinema_id: int, admin_id: int) -> None:
    conn = get_conn()
    cur = conn.cursor()
    dt_str = date_time.strftime('%Y-%m-%d %H:%M:%S')
    cur.execute(
        "UPDATE Schedule SET date_time = ?, Film_ID = ?, Cinema_ID = ?, admin_id = ? WHERE Schedule_ID = ?",
        (dt_str, film_id, cinema_id, admin_id, schedule_id)
    )
    conn.commit()
    conn.close()


def delete(schedule_id: int) -> None:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM Schedule WHERE Schedule_ID = ?", (schedule_id,))
    conn.commit()
    conn.close()