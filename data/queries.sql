-- Запросы для работы в postgre SQL--

-- Вывести список всех компаний и количество вакансий открытых в г.Москва --

SELECT employers.name_employer AS company_name,
COUNT(vacancies.id_vacancy) AS count_of_vacancies
FROM employers
JOIN vacancies ON employers.id_employer = vacancies.id_employer
WHERE vacancies.city = 'Москва'
GROUP BY employers.name_employer
ORDER BY count_of_vacancies DESC;

-- Вывести среднюю зарплату по вакансиям в г.Москва --

SELECT FLOOR(AVG(salary_avg)) AS average_salary
FROM vacancies
WHERE salary_avg IS NOT NULL AND city = 'Москва';

-- Вывести названия компаний,вакакнсий и ссылки на них где есть слово "python" --

SELECT employers.name_employer, vacancies.name_vacancy, vacancies.url
FROM employers
JOIN vacancies ON employers.id_employer = vacancies.id_employer
WHERE LOWER(vacancies.name_vacancy) LIKE '%python%';

-- Вывести компанию, название вакансии, город, среднюю зарплату, ссылку, где зп выше средней.
WITH AverageSalary AS (
SELECT FLOOR(AVG(salary_avg)) AS avg_salary
FROM vacancies
WHERE salary_avg IS NOT NULL)

SELECT
    employers.name_employer,
    vacancies.name_vacancy,
    vacancies.city,
    vacancies.salary_avg AS salary,
    vacancies.url AS vacancy_url
FROM employers
JOIN vacancies ON employers.id_employer = vacancies.id_employer, AverageSalary
WHERE vacancies.salary_avg > AverageSalary.avg_salary;