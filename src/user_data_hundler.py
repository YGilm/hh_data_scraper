from db_manager import *
from config import config
from hh_data import *


class UserDataHandler:
    def __init__(self, hh_database):
        """Инициализация обработчика данных пользователя с созданием базы данных."""
        params = config()
        self.db = DBCreate(hh_database, params)
        self.db.create_database()

    def process_company_data(self, company_name: str) -> list:
        """Обрабатывает данные компании и сохраняет их в базу данных."""

        print(f"Поиск данных для компании {company_name}...")
        print("Это может занять некоторое время, пожалуйста, подождите.")

        hh = Employers(company_name)
        data = hh.get_request
        self.db.save_employers_to_database(data)

        return data

    def process_vacancy_data(self, company_data: list):
        """Обрабатывает данные о вакансиях и сохраняет их в базу данных"""

        for index, value in enumerate(company_data):
            id_emp = value["id"]
            vac = Vacancy(id_emp)
            vacancy_list = vac.put_vacancies_in_list()
            self.db.save_vacancies_to_database(vacancy_list)

    def user_interaction(self):
        """Взаимодействие с пользователем для выбора компаний и загрузки данных."""

        request_count = 1
        list_emp = []

        while request_count <= 10:
            customers_word = input("Введите название компании которую будем отслеживать: ")
            list_emp.append(customers_word)

            company_data = self.process_company_data(customers_word)
            self.process_vacancy_data(company_data)

            request_count += 1
