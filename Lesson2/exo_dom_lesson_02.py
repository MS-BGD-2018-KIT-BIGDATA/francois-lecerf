import requests
from bs4 import BeautifulSoup
import re


def getSoupFromURL(url, method='get', data={}):

    # choix de la methode http
    if method == 'get':
        res = requests.get(url)
    elif method == 'post':
        res = requests.post(url, data=data)
    else:
        return None

    # page web trouvee
    if res.status_code == 200:
        soup = BeautifulSoup(res.text, 'html.parser')
        return soup
    else:
        return None

    def getNumberOfSharesForPage(url, classname):
        soup = getSoupFromURL(url)
        if soup:
            share_content = soup.find_all(class_=classname).text.strip()
        print(share_content)
        # if 'K' in share_content:
        # remove the K at the end with -1
        #  parts = share_content[:-1].split(',')
        #  return int(parts[0])*1000 + int(parts[1])*100
        # else:
        #  return int(share_content)
    else:
        return None




url_search = "http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice="

classname = 'montantpetit G'


for date in ('2010', '2011', '2012', '2013', '2014', '2015'):
    print("Extraction : " + date)
    soup = getSoupFromURL(url_search + date)

    if soup:
        # share_content = soup.find_all(class_=classname)
        share_content = soup.find_all(class_=classname)
        # [0].text.strip()
        index = (1, 2, 4, 5, 10, 11, 13, 14)
        for i in index:
            print(share_content[i].text.strip())
