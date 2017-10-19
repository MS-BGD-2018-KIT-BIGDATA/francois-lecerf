from bs4 import BeautifulSoup
import requests
import unicodedata
from multiprocessing import Pool
import pandas as pd
import re
from collections import namedtuple


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


def data_cleanup(parameters, value):
    if "itemprop" not in parameters:
        price = PRICE_PATTERN.search(value)
        distance = DISTANCE_PATTERN.search(value)
        #print(parameters, "/", value)
        # print(price)
        # print(distance)
        if price:
            return ['PRIX', value]
        elif distance:
            return ['DISTANCE', value]
        else:
            return None
    elif (parameters["itemprop"] == "model"):
        return ['MODELE', value]
    elif (parameters["itemprop"] == "brand"):
        return ['MARQUE', value]
    elif (parameters["itemprop"] == "releaseDate"):
        return ['ANNEE', value]
    else:
        # print("toto")
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
    # outputs NamedTuple
    output = None
    soup = getSoupFromURL(url)
    if(soup):
        tag_list = soup.findAll("span", class_="value")
        property_tuples = [(tag.attrs, unicodedata.normalize(
                           "NFKD", tag.text.strip().lower())) for tag in tag_list]
        tmp_table = [data_cleanup(parameters, value)
                     for parameters, value in property_tuples]
        tmp_dict = dict([row for row in tmp_table if row != None])
        output = Vehicle(MARQUE=tmp_dict.get('MARQUE'),
                         MODELE=tmp_dict.get('MODELE'),
                         ANNEE=tmp_dict.get('ANNEE'),
                         DISTANCE=tmp_dict.get('DISTANCE'),
                         PRIX=tmp_dict.get('PRIX'))
    return output


PRICE_PATTERN = re.compile("[0-9]*\ ?[0-9]*\ *€")
DISTANCE_PATTERN = re.compile("[0-9]*\ ?[0-9]*\ *km")

Vehicle = namedtuple(
    'Vehicle', ['MARQUE', 'MODELE', 'ANNEE', 'DISTANCE', 'PRIX'])

pool = Pool(10)

vehicles = pool.map(get_single_result, get_results())

pd.DataFrame(vehicles, columns=Vehicle._fields)
