from repositories import schedule_rep, film_rep, cinema_rep
import datetime


def create_schedule(date_time: datetime.datetime, film_id: int, cinema_id: int, admin_id: int, user_role_id: int):
    # 1. Проверка прав
    if user_role_id != 1:
        raise Exception("Только администратор может создавать сеансы")

    # 2. Проверка существования фильма
    if not film_rep.get_by_id(film_id):
        raise Exception("Фильм с таким ID не найден")

    # 3. Проверка существования кинотеатра
    if not cinema_rep.get_by_id(cinema_id):
        raise Exception("Кинотеатр с таким ID не найден")

    # 4. Проверка даты (нельзя создать сеанс в прошлом)
    if date_time < datetime.datetime.now():
        raise Exception("Нельзя создать сеанс в прошлом")

    # Если все проверки пройдены - создаем
    schedule_rep.create(date_time, film_id, cinema_id, admin_id)


def get_all_schedules():
    return schedule_rep.get_all()