from ui.auth import login, register
from ui.menus import admin_menu, client_menu

def main():
    while True:
        print("\n========== КИНОСЕАНСЫ ==========")
        print("1. Войти")
        print("2. Зарегистрироваться (для клиентов)")
        print("0. Выйти из программы")
        choice = input("Выберите действие: ")

        if choice == "1":
            user = login()
            if user:

                if user.userrole_id == 1 or user.userrole_id == 2:
                    admin_menu(user)
                else:
                    client_menu(user)

        elif choice == "2":
            register()

        elif choice == "0":
            print("До свидания!")
            break
        else:
            print("Неверный пункт меню.")

if __name__ == "__main__":
    main()