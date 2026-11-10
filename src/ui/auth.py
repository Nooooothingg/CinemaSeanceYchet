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
    print("\n--- Регистрация ---")
    username = input("Ваше имя: ")
    login_value = input("Придумайте логин: ")
    password_value = input("Придумайте пароль: ")
    secret_word = input("Секретное слово для регистрации администратора (или оставьте пустым для клиента): ")

    try:
        role_id = auth.register_with_secret(username, login_value, password_value, secret_word)
        if role_id == auth.SYSADMIN_ROLE_ID:
            print("\nРегистрация прошла успешно! Вы зарегистрированы как системный администратор.")
        else:
            print("\nРегистрация прошла успешно! Вы зарегистрированы как клиент. Теперь вы можете войти.")
    except Exception as e:
        print(f"\n[ОШИБКА] {e}")