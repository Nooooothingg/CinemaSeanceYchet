from repositories import users_rep
from src.repositories import user_role_rep

SYSADMIN_ROLE_ID = 1
ADMIN_ROLE_ID = 2
CLIENT_ROLE_ID = 3



def login(login_value: str, password_value: str):
    if not login_value.strip() or not password_value.strip():
        raise Exception("Логин и пароль не могут быть пустыми")

    user = users_rep.get_by_login(login_value)

    if not user or user.passwordhash != password_value:
        raise Exception("Неверный логин или пароль")

    return user


def register(username: str, login: str, password: str, role_id: int):
    if not username.strip() or not login.strip() or not password.strip():
        raise Exception("Все поля обязательны для заполнения")

    if users_rep.get_by_login(login):
        raise Exception("Пользователь с таким логином уже существует")

    users_rep.create(role_id, username, login, password)