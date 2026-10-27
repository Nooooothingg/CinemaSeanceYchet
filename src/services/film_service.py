from repositories import film_rep


def create_film(film_name: str, film_descr: str | None, film_time: int, user_role_id: int):
    # Проверка прав (только админ может добавлять фильмы)
    if user_role_id == 3:  # 1 - это ID роли админа (замените на ваш)
        raise Exception("Только администратор может добавлять фильмы")

    if not film_name.strip():
        raise Exception("Название фильма не может быть пустым")

    if film_time <= 0:
        raise Exception("Длительность фильма должна быть больше нуля")

    film_rep.create(film_name, film_descr, film_time)


def get_all_films():
    return film_rep.get_all()