"""
Быстрый старт с GitHub API
Показывает список всех репозиториев ползователя, сохраняет полный ответ в файл

"""

import requests
import json

params = {'login': 'miguelgrinberg',
          'private': False,
          'per_page': 50,
          'page': 1}

url_user = f"https://api.github.com/users/{params['login']}"  # пользователь и информ. о нем
url_repos = f"https://api.github.com/users/{params['login']}/repos"  # все репозитории пользователя и информ. о них


def show_repos_list():
    response_1 = requests.get(url=url_user, params=params)
    j_data_user = response_1.json()
    print(f"Total public repositories for this user is {j_data_user['public_repos']}")
    while True:
        response_2 = requests.get(url=url_repos, params=params)
        j_data_repos = response_2.json()
        if len(j_data_repos) == 0:
            break
        for repo in j_data_repos:
            print(repo['html_url'])
        params['page'] += 1
        print(params['page'])

        with open('json_data.json', 'a+') as outfile:
            json.dump(j_data_repos, outfile, indent=2)


if __name__ == "__main__":
    show_repos_list()
