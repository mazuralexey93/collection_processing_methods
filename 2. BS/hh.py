"""
Необходимо собрать информацию о вакансиях на вводимую должность (используем input или через аргументы получаем должность) с сайта HH
Приложение должно анализировать несколько страниц сайта (также вводим через input или аргументы). Получившийся список должен содержать в себе минимум:
Наименование вакансии.
Предлагаемую зарплату (разносим в три поля: минимальная и максимальная и валюта. цифры преобразуем к цифрам).
Ссылку на саму вакансию.
Сайт, откуда собрана вакансия. (можно прописать статично hh.ru или superjob.ru)

"""
import requests
from bs4 import BeautifulSoup
from pprint import pprint

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

vacancies = dom.find_all('div', {'class': 'vacancy-serp-item__layout'})
pages = dom.find_all('a', {'data-qa': 'pager-page'})
last_page = int(list(pages)[-1].find('span').text)
vacancy_list = []

for i in range(last_page):
    params['page'] = i
    print(f'Scrapping page № {params["page"] + 1}')
    params['page'] += 1
    for vacancy in vacancies:
        vacancy_data = {}
        salary_dict = {'min': None, 'max': None, 'currency': None}

        name = vacancy.find('a', {'class': 'bloko-link'})
        link = name.get('href')
        name = name.text
        try:
            salary = vacancy.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'}).text
            if salary:
                splitted_salary = salary.replace('\u202f', '').split(" ")
                if splitted_salary[0] == 'от':
                    salary_dict['min'] = int(splitted_salary[1])
                elif splitted_salary[0] == 'до':
                    salary_dict['max'] = int(splitted_salary[1])
                else:
                    salary_dict['min'] = int(splitted_salary[0])
                    salary_dict['max'] = int(splitted_salary[2])

                salary_dict['currency'] = splitted_salary[-1]
        except:
            salary_dict = salary_dict

        vacancy_data['site'] = 'hh.ru'
        vacancy_data['name'] = name
        vacancy_data['link'] = link
        vacancy_data['salary'] = salary_dict

        vacancy_list.append(vacancy_data)

pprint(vacancy_list)
print(len(vacancy_list))

