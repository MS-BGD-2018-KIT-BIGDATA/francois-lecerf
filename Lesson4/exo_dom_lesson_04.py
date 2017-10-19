from bs4 import BeautifulSoup
import requests
import unicodedata
from multiprocessing import Pool
import numpy as np
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
            return ['PRIX', NUMERIC_PATTERN_TRIM.sub('', value)]
        elif distance:
            return ['DISTANCE', NUMERIC_PATTERN_TRIM.sub('', value)]
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


def get_results(region = "ile_de_france",question="zoe"):
    url = ('https://www.leboncoin.fr/voitures/offres/'
           + region
           + '/occasions/?th=1&q='
           + question)
    output = []
    soup = getSoupFromURL(url)
    if(soup):
        temp_table = soup.find("main").find("section").find(
            "section").find("section").find("section").find("ul")
        rows = temp_table.find_all("li")
        output = ["https:" + row.find("a").get('href') for row in rows]
    return output


def get_single_result(url):
    # outputs Vehicle NamedTuple
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


def get_argus_price(url):
    soup = getSoupFromURL(url)
    output = None
    if(soup):
        output = NUMERIC_PATTERN_TRIM.sub(
            '', unicodedata.normalize("NFKD",soup.find(class_="jsRefinedQuot").text.strip().lower()))
    return output


def get_results_argus():
    url_root = "https://www.lacentrale.fr/"
    url = url_root + "cote-voitures-renault-zoe--2013-.html"
    output = []
    soup = getSoupFromURL(url)
    if(soup):
        tmp_tag = soup.find(class_="listingResult").find_all(class_="listingResultLine auto")
        tmp_list = [(tag.find("h3").text.strip().lower(), url_root + tag.find("a").get('href')) for tag in tmp_tag]
        #a multithreader
        output = [ArgusVehicle(MODELE=modele, PRIX=get_argus_price(url))
                  for (modele, url) in tmp_list]
    return output


# nettoyage des valeurs numeriques
PRICE_PATTERN = re.compile("[0-9]*\ ?[0-9]*\ *€")
DISTANCE_PATTERN = re.compile("[0-9]*\ ?[0-9]*\ *km")
NUMERIC_PATTERN_TRIM = re.compile(r'[^\d.,]+')

# modele de donnees
Vehicle = namedtuple('Vehicle', ['MARQUE', 'MODELE', 'ANNEE', 'DISTANCE', 'PRIX'])
Region = namedtuple('Region', ['REGION'])
RegionVehicle = namedtuple('RegionVehicle', Region._fields + Vehicle._fields)
ArgusVehicle = namedtuple('ArgusVehicle', ['MODELE', 'PRIX'])

#Argus des zoe
df_argus_vehicles = pd.DataFrame(get_results_argus(), columns=ArgusVehicle._fields)


# liste des regions
regions = ['aquitaine','ile_de_france','provence_alpes_cote_d_azur']

# Liste des annonces a crawler
annonces = dict([(region, get_results(region=region, question="zoe")) for region in regions])

#Lancement du multithread sur chaque annonce (mal gere ...)
pool = Pool(10)
region_vehicles = []
for region in regions:
    vehicles = pool.map(get_single_result, annonces[region])
    region_vehicles += [RegionVehicle(*(Region(region) + vehicle)) for vehicle in vehicles]

#creation du tableau pandas
vehicles_type = {'REGION':str, 'MARQUE': str, 'MODELE': str,
                 'ANNEE':np.int32, 'DISTANCE':np.float64, 'PRIX':np.float64}
# df_vehicles = pd.DataFrame(vehicles, dtype=vehicles_type, columns=Vehicle._fields)
df_region_vehicles = pd.DataFrame(region_vehicles, columns=RegionVehicle._fields)

for k, v in vehicles_type.items():
    df_region_vehicles[k] = df_region_vehicles[k].astype(v)

print(df_argus_vehicles.head())
print(df_region_vehicles.head())
