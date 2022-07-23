"""
2. Написать функцию, которая производит поиск и выводит на экран вакансии с заработной платой больше введённой суммы
 (необходимо анализировать оба поля зарплаты). То есть цифра вводится одна, а запрос проверяет оба поля
"""
from pymongo import MongoClient
from pprint import pprint

client = MongoClient('127.0.0.1', 27017)
db = client['all_vacancies']
vacancies_collection = db.vacancies_collection


def vacancy_filter(vacancies, gain):
    both_limit = {'$or': [{'salary_min': {'$gt': gain}},
                          {'salary_max': {'$gte': gain}}],
                  '$and': [{'salary_cur': 'руб.'}]}

    return list(vacancies.find(both_limit))


pprint(vacancy_filter(vacancies_collection, 199000))
pprint(len(vacancy_filter(vacancies_collection, 199000)))
