import time
from config import config
from src.db_manager import DBManager
from src.user_data_hundler import UserDataHandler


def main():
    """Основная функция интерактивного приложения для работы с базой данных вакансий."""

    print("Здравствуйте! Давайте найдём компании и их вакансии.")
    print("Запишем в базу данных 10 компаний и их вакансии которые будем отслеживать")
    # Azur Games, Crazy Panda, Ozon, ChillBase, Tinkoff, Avito, Yota, ВСК, Sber, Tele2

    params = config()
    database_name = 'hh_database'
    user_handler = UserDataHandler(database_name)
    user_handler.user_interaction()

    db_manager = DBManager(database_name, params)

    while True:
        print(
            """\nВыберите что хотите вывести на экран:
            1. Все компании и количество вакансий
            2. Все вакансии в выбраных компаниях
            3. Среднюю зарплату по вакансиям
            4. Вакансии с зарплатой выше средней
            5. Отфильтровать вакансии по ключевому слову
            0. Выход"""
        )

        user_number = input("\nВведите номер выбранного вами действия: ")

        if user_number == "1":
            data = db_manager.get_companies_and_vacancies_count()
            db_manager.pretty_print(data)

        elif user_number == "2":
            for idx, vacancy in enumerate(db_manager.get_all_vacancies(), 1):
                if idx > 50:
                    break
                db_manager.pretty_print(vacancy)

        elif user_number == "3":
            avg_salary = db_manager.get_avg_salary()
            print(f"Средняя зарплата по всем вакансиям: {avg_salary}")

        elif user_number == "4":
            for idx, vacancy in enumerate(db_manager.get_vacancies_with_higher_salary(), 1):
                if idx > 50:
                    break
                db_manager.pretty_print(vacancy)

        elif user_number == "5":
            word = input("Введите ключевое слово для поиска: ")
            for vacancy in db_manager.get_vacancies_with_keyword(word):
                db_manager.pretty_print(vacancy)

        elif user_number == "0":
            # Выход из программы.
            print("Выход из программы...")
            time.sleep(1)
            print("До свидания!")
            break

        else:
            print("Неправильный ввод, попробуйте еще раз.")


if __name__ == "__main__":
    main()
