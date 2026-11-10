from repositories import users_rep
from src.repositories import user_role_rep
from src.utils.password import hash_password, verify_password

SYSADMIN_ROLE_ID = 1
ADMIN_ROLE_ID = 2
CLIENT_ROLE_ID = 3

SECRET_ADMIN_WORD = "kinoseans2026"


def login(login_value: str, password_value: str):
    if not login_value.strip() or not password_value.strip():
        raise Exception("Логин и пароль не могут быть пустыми")

    user = users_rep.get_by_login(login_value)

    if not user or not verify_password(password_value, user.passwordhash):
        raise Exception("Неверный логин или пароль")

    return user


def register(username: str, login: str, password: str, role_id: int):
    if not username.strip() or not login.strip() or not password.strip():
        raise Exception("Все поля обязательны для заполнения")

    if users_rep.get_by_login(login):
        raise Exception("Пользователь с таким логином уже существует")

    password_hash = hash_password(password)
    users_rep.create(role_id, username, login, password_hash)


def register_with_secret(username: str, login: str, password: str, secret_word: str):
    """
    Регистрация с секретным словом. Если слово верное — создаёт системного администратора (role_id=1),
    иначе — обычного клиента (role_id=3).
    """
    if not username.strip() or not login.strip() or not password.strip():
        raise Exception("Все поля обязательны для заполнения")

    if users_rep.get_by_login(login):
        raise Exception("Пользователь с таким логином уже существует")

    if secret_word.strip() == SECRET_ADMIN_WORD:
        role_id = SYSADMIN_ROLE_ID
    else:
        role_id = CLIENT_ROLE_ID

    password_hash = hash_password(password)
    users_rep.create(role_id, username, login, password_hash)
    return role_id


def register_cinema_admin(username: str, login: str, password: str):
    """
    Регистрация администратора кинотеатра (role_id=2). Доступно только системному администратору.
    """
    if not username.strip() or not login.strip() or not password.strip():
        raise Exception("Все поля обязательны для заполнения")

    if users_rep.get_by_login(login):
        raise Exception("Пользователь с таким логином уже существует")

    password_hash = hash_password(password)
    users_rep.create(ADMIN_ROLE_ID, username, login, password_hash)