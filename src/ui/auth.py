from services import auth


def login():
    print("\n--- Вход в систему ---")
    login_value = input("Логин: ")
    password_value = input("Пароль: ")

    try:
        user = auth.login(login_value, password_value)
        print(f"\nУспешный вход! Добро пожаловать, {user.username}.")
        return user
    except Exception as e:
        print(f"\n[ОШИБКА] {e}")
        return None


def register():
    print("\n--- Регистрация клиента ---")
    username = input("Ваше имя: ")
    login_value = input("Придумайте логин: ")
    password_value = input("Придумайте пароль: ")

    try:
        # По умолчанию регистрируем клиента (ID роли 2)
        auth.register(username, login_value, password_value, role_id=2)
        print("\nРегистрация прошла успешно! Теперь вы можете войти.")
    except Exception as e:
        print(f"\n[ОШИБКА] {e}")