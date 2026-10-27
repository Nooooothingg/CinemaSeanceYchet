from services import film_service, schedule_service


def admin_menu(user):
    while True:
        print(f"\n===== МЕНЮ АДМИНИСТРАТОРА ({user.username}) =====")
        print("1. Добавить фильм")
        print("2. Посмотреть все фильмы")
        print("3. Добавить сеанс в расписание")
        print("4. Посмотреть все сеансы")
        print("0. Выйти из аккаунта")
        choice = input("Выберите действие: ")

        if choice == "1":
            film_name = input("Название фильма: ")
            film_descr = input("Описание (можно пропустить): ")
            try:
                film_time = int(input("Длительность в минутах: "))
                film_service.create_film(film_name, film_descr, film_time, user.userrole_id)
                print("Фильм успешно добавлен!")
            except ValueError:
                print("[ОШИБКА] Длительность должна быть числом.")
            except Exception as e:
                print(f"[ОШИБКА] {e}")

        elif choice == "2":
            films = film_service.get_all_films()
            print("\n--- Список фильмов ---")
            for f in films:
                print(f"ID: {f.film_id} | {f.film_name} | {f.film_time} мин.")

        elif choice == "3":
            print("\n(Подсказка: сначала посмотрите ID фильмов и кинотеатров)")
            try:
                film_id = int(input("ID фильма: "))
                cinema_id = int(input("ID кинотеатра: "))
                date_str = input("Дата и время (ГГГГ-ММ-ДД ЧЧ:ММ): ")

                # Конвертация строки в datetime
                import datetime
                date_time = datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M")

                schedule_service.create_schedule(date_time, film_id, cinema_id, user.user_id, user.userrole_id)
                print("Сеанс успешно добавлен в расписание!")
            except ValueError:
                print("[ОШИБКА] Неверный формат ввода числа или даты.")
            except Exception as e:
                print(f"[ОШИБКА] {e}")

        elif choice == "4":
            schedules = schedule_service.get_all_schedules()
            print("\n--- Расписание сеансов ---")
            for s in schedules:
                print(f"{s.date_time} | Фильм: {s.film_name} | Зал: {s.cinema_name}")

        elif choice == "0":
            print("Выход из аккаунта...")
            break
        else:
            print("Неверный пункт меню.")


def client_menu(user):
    while True:
        print(f"\n===== МЕНЮ КЛИЕНТА ({user.username}) =====")
        print("1. Посмотреть расписание сеансов")
        print("0. Выйти из аккаунта")
        choice = input("Выберите действие: ")

        if choice == "1":
            schedules = schedule_service.get_all_schedules()
            print("\n--- Расписание сеансов ---")
            if not schedules:
                print("Сеансов пока нет.")
            for s in schedules:
                print(f"{s.date_time} | Фильм: {s.film_name} | Зал: {s.cinema_name}")

        elif choice == "0":
            print("Выход из аккаунта...")
            break
        else:
            print("Неверный пункт меню.")