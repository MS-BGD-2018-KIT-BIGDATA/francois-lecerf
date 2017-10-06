import requests
from bs4 import BeautifulSoup
import requests
import json
import pandas as pd
from multiprocessing import Pool
from operator import itemgetter

def getAuthentification():
    with open('secret', 'r', encoding='utf8') as input_file:
        login, pwd = input_file.readline().strip().split(' ')
    return login, pwd


def getSoupFromURL(url, method='get', data={}):
    if method == 'get':
        res = requests.get(url)
    elif method == 'post':
        res = requests.post(url, data=data)
    else:
        return None

    if res.status_code == 200:
        soup = BeautifulSoup(res.text, 'html.parser')
        return soup
    else:
        return None


def getUserStats(user):
    url_api = ("/".join(['https://api.github.com/users', user, "starred"]))
    r = requests.get(url_api, auth=(LOGIN, PWD))
    if (r.ok):
        json_contents = json.loads(r.text)
        df_starred = pd.DataFrame([(project['id'], project['stargazers_count'])
                                  for project in json_contents],
                                  columns=['id', 'stargazers_count'])
        return(df_starred.stargazers_count.mean())
    else:
        return None


def getListOfUsers():
    url_api = 'https://gist.github.com/paulmillr/2657075'
    soup = getSoupFromURL(url_api)
    if (soup):
        temp_table = soup.find("table").find("tbody")
        rows = temp_table.find_all("tr")
    github_users = []
    for row in rows:
        github_users.append(row.find("a").text.strip())
    return github_users


github_users = getListOfUsers()
print(github_users)
LOGIN, PWD = getAuthentification()
# no multithread
# for user in github_users:
#    temp = getUserStats(user)
#    print(user, temp)
# multithread
p = Pool(6)
stats = p.map(getUserStats, github_users)
result = sorted([(user, stat) for user, stat in zip(github_users, stats)
                 ], key=itemgetter(1), reverse=True)
print(result)
