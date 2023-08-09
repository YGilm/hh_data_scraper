import time
import requests


class Employers:
    def __init__(self, data: str):
        self.data = data

    @property
    def get_request(self):
        employers = []
        per_page = 50
        page = 0
        while True:
            params = {
                "text": self.data,
                "area": 113,
                "only_with_vacancies": True,
                "page": page,
                "per_page": per_page,
            }
            response = requests.get('https://api.hh.ru/employers', params=params)
            response.raise_for_status()
            data = response.json()
            employers.extend(data["items"])
            if len(data["items"]) < per_page:
                break
            page += 1
            time.sleep(0.22)
        return employers


class Vacancy:
    def __init__(self, id_employer):
        self.id_employer = id_employer

    def get_vacancy(self):
        vacancies = []
        per_page = 50
        page = 0
        retries = 3

        while retries:
            params = {
                "employer_id": self.id_employer,
                "page": page,
                'per_page': per_page,
            }
            response = requests.get('https://api.hh.ru/vacancies', params=params)
            if response.status_code == 400:
                print(f"Ошибка 400 при запросе на страницу {page}. Вакансии в пределах лимита получены")
                break
            response.raise_for_status()
            data = response.json()
            vacancies.extend(data.get('items', []))
            if len(data.get('items', [])) < per_page:
                break
            page += 1
            time.sleep(0.22)
            retries = 3
        return vacancies

    def put_vacancies_in_list(self):
        """Записывает найденные вакансии с нужными ключами в список словарей"""
        vacancies_list = []
        for item in self.get_vacancy():
            salary = item.get('salary') or {}
            salary_from = salary.get('from') or 0
            salary_to = salary.get('to') or 0
            employer = item.get('employer') or {}
            area = item.get('area') or {}
            snippet = item.get('snippet') or {}
            vacancy = {
                'id_vacancy': item.get('id'),
                'name_vacancy': item.get('name'),
                'id_employer': employer.get('id', 0),
                'name_employer': employer.get('name', "Не указано"),
                'city': area.get('name', "Не указано"),
                'salary_from': salary_from,
                'salary_to': salary_to,
                'salary_avg': (salary_from if salary_to == 0 else (salary_from + salary_to) / 2) or (
                    salary_to if salary_from == 0 else 0),
                'experience': item['experience'].get('name'),
                'url': item.get('alternate_url'),
                "requirement": snippet.get('requirement', "Не указано"),
            }
            vacancies_list.append(vacancy)
        return vacancies_list
