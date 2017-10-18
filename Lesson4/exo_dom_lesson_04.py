from bs4 import BeautifulSoup
import requests
import unicodedata
from multiprocessing import Pool
import pandas as pd
import re


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


def get_results(question="zoe"):
    url = 'https://www.leboncoin.fr/voitures/offres/ile_de_france/occasions/?th=1&q=' + question
    output = []
    soup = getSoupFromURL(url)
    if(soup):
        temp_table = soup.find("main").find("section").find(
            "section").find("section").find("section").find("ul")
        rows = temp_table.find_all("li")
        output = ["https:" + row.find("a").get('href') for row in rows]
    return output


def get_single_result(url):
    output = []
    soup = getSoupFromURL(url)
    if(soup):
        tag_list = soup.findAll("span", class_="value")
        output = [(tag.attrs, unicodedata.normalize(
            "NFKD", tag.text.strip())) for tag in tag_list]
    return output


pool = Pool(10)

stats = pool.map(get_single_result, get_results())

print(stats)
