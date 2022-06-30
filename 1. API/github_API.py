"""
Быстрый старт с GitHub API
Показывает список всех репозиториев ползователя
* Показывает список только с первой страницы (т.е ограничение 30)

* curl https://api.github.com/users/mazuralexey93/repos >> curl_repos_list.json

"""

import requests
import json

params = {'login': 'mazuralexey93',
          'private': False}

url_repos = f"https://api.github.com/users/{params['login']}/repos"
url_user = f"https://api.github.com/users/{params['login']}"

response_1 = requests.get(url=url_user, params=params)
response_2 = requests.get(url=url_repos, params=params)

j_data_1 = response_1.json()
j_data_2 = response_2.json()


def show_repos_list():
    print(f"Total public repositories for this user is {j_data_1['public_repos']}")
    for repo in j_data_2:
        print(repo['html_url'])


def save_outfile():
    with open('json_data.json', 'w') as outfile:
        json.dump(j_data_2, outfile, indent=2)


if __name__ == "__main__":
    show_repos_list()
    save_outfile()
