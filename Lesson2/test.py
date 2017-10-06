import requests
from bs4 import BeautifulSoup
response = requests.get("http://alize2.finances.gouv.fr/communes/eneuro\
/detail.php?icom=056&dep=075&type=BPS&param=5&exercice=2013")

print(response.status_code)
if response.status_code == 200:
    # print(response.content)
    soup = BeautifulSoup(response.content, 'html.parser')

test = ("C est une maison bleue "
        "Accrochee a ma memoire")

print(test)
