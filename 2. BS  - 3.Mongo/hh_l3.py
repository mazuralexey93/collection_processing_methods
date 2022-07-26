"""
Необходимо собрать информацию о вакансиях на вводимую должность (используем input или через аргументы получаем должность) с сайта HH
Приложение должно анализировать несколько страниц сайта (также вводим через input или аргументы). Получившийся список должен содержать в себе минимум:
Наименование вакансии.
Предлагаемую зарплату (разносим в три поля: минимальная и максимальная и валюта. цифры преобразуем к цифрам).
Ссылку на саму вакансию.
Сайт, откуда собрана вакансия. (можно прописать статично hh.ru или superjob.ru)

1. Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и реализовать функцию,
 которая будет добавлять только новые вакансии/продукты в вашу базу.
2. Написать функцию, которая производит поиск и выводит на экран вакансии с заработной платой больше введённой суммы
 (необходимо анализировать оба поля зарплаты). То есть цифра вводится одна, а запрос проверяет оба поля
"""
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from pymongo import errors
from pprint import pprint


def search_vacancies_hh():
    client = MongoClient('127.0.0.1', 27017)  #
    db = client['all_vacancies']  # database                            # Mongo db stuff
    vacancies_collection = db.vacancies_collection  #

    url = 'https://spb.hh.ru/search/vacancy'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36 OPR/88.0.4412.40'}

    params = {
        'text': 'python',
        'items_on_page': 20
    }

    session = requests.Session()
    response = session.get(url=url, headers=headers, params=params)

    dom = BeautifulSoup(response.text, 'html.parser')

    vacancies = dom.find_all('div', {'class': 'vacancy-serp-item__layout'})  #
    pages = dom.find_all('a', {'data-qa': 'pager-page'})  # Beautiful soup stuff
    last_page = int(list(pages)[-1].find('span').text)  #
    vacancy_list = []

    added_counter = 0
    skipped_counter = 0

    for i in range(last_page):
        params['page'] = i
        params['page'] += 1

        for vacancy in vacancies:
            vacancy_data = {}

            salary_max, salary_min, salary_cur = None, None, None

            name = vacancy.find('a', {'class': 'bloko-link'})
            link = name.get('href')
            name = name.text

            try:
                salary = vacancy.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'}).text
                if salary:
                    splitted_salary = salary.replace('\u202f', '').split(" ")
                    if splitted_salary[0] == 'от':
                        salary_min = int(splitted_salary[1])
                    elif splitted_salary[0] == 'до':
                        salary_max = int(splitted_salary[1])
                    else:
                        salary_min = int(splitted_salary[0])
                        salary_max = int(splitted_salary[2])

                    salary_cur = splitted_salary[-1]
            except:
                ...  # salary_max, salary_min, salary_cur = None, None, None

            vacancy_data['site'] = 'hh.ru'
            vacancy_data['name'] = name
            vacancy_data['link'] = link
            vacancy_data['salary_max'] = salary_max
            vacancy_data['salary_min'] = salary_min
            vacancy_data['salary_cur'] = salary_cur
            vacancy_data['_id'] = link

            vacancy_list.append(vacancy_data)

            try:
                vacancies_collection.insert_one(vacancy_data)
                added_counter += 1
            except errors.DuplicateKeyError:
                vacancies_collection.replace_one({'_id': vacancy_data.get('_id')}, vacancy_data)
                skipped_counter += 1

    print(f'added : {added_counter}, \nskipped : {skipped_counter}')


if __name__ == "__main__":
    search_vacancies_hh()
