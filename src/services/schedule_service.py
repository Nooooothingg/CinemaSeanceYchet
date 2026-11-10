from repositories import schedule_rep, film_rep, cinema_rep
import datetime


def create_schedule(date_time: datetime.datetime, film_id: int, cinema_id: int, admin_id: int, user_role_id: int):
    # 1. Проверка прав (системный администратор или администратор кинотеатра)
    if user_role_id not in (1, 2):
        raise Exception("Только администратор может создавать сеансы")

    # 2. Проверка существования фильма
    film = film_rep.get_by_id(film_id)
    if not film:
        raise Exception("Фильм с таким ID не найден")

    # 3. Проверка существования кинотеатра
    if not cinema_rep.get_by_id(cinema_id):
        raise Exception("Кинотеатр с таким ID не найден")

    # 4. Проверка даты (нельзя создать сеанс в прошлом)
    if date_time < datetime.datetime.now():
        raise Exception("Нельзя создать сеанс в прошлом")

    # 5. Проверка наложения сеансов в одном кинотеатре
    new_end = date_time + datetime.timedelta(minutes=int(film.film_time))
    existing_schedules = schedule_rep.get_by_cinema(cinema_id)
    for existing in existing_schedules:
        existing_end = existing.date_time + datetime.timedelta(minutes=int(existing.film_time or 0))
        if date_time < existing_end and new_end > existing.date_time:
            raise Exception(
                f"Сеанс накладывается на существующий: {existing.date_time} - {existing_end} "
                f"(фильм: {existing.film_name})"
            )

    # Если все проверки пройдены - создаем
    schedule_rep.create(date_time, film_id, cinema_id, admin_id)


def get_all_schedules():
    return schedule_rep.get_all()