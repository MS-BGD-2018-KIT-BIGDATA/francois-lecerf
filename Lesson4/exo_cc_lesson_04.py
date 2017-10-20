import requests
import json
import pandas as pd

def get_medicaments(medic_name):
    url_api = ("https://www.open-medicaments.fr/api/v1/medicaments?query=" + medic_name)
    r = requests.get(url_api)
    if (r.ok):
            json_contents = json.loads(r.text)
            list_medic = [(medicament['codeCIS'], medicament['denomination'])
                          for medicament in json_contents]
            df_medicaments = pd.DataFrame(list_medic, columns = ["codeCIS", "denomination"])
            return df_medicaments

get_medicaments("ibuprofene")

def get_medicament_details(codeCIS):
    url_api = "https://www.open-medicaments.fr/api/v1/medicaments/" + codeCIS
    r = requests.get(url_api)
    if (r.ok):
            json_contents = json.loads(r.text)
            #list_medic = [(medicament['codeCIS'], medicament['denomination'])
            #              for medicament in json_contents]
            #df_medicaments = pd.DataFrame(list_medic, columns = ["codeCIS", "denomination"])
            return json_contents

get_medicaments("ibuprofene")
print(get_medicament_details("64565560"))
