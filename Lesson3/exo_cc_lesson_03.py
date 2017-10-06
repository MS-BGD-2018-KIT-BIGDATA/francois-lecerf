import requests
from bs4 import BeautifulSoup
import re

def getSoupFromURL(url, method='get', data={}):

  #choix de la methode http
    if method == 'get':
        res = requests.get(url)
    elif method == 'post':
        res = requests.post(url, data=data)
    else:
        return None

  #page web trouvee
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
    #if 'K' in share_content:
      #remove the K at the end with -1
    #  parts = share_content[:-1].split(',')
    #  return int(parts[0])*1000 + int(parts[1])*100
    #else:
    #  return int(share_content)
  else:
    return None



url_search = "https://www.cdiscount.com/informatique/ordinateurs-pc-portables/acer-pc-portable-swift-sf113-31-c7gq-13-fhd-ips/f-10709-nxgpnef001.html#mpos=5|cd"

price_block_classname = "fTopPrice jsContent"

striked_price_classname = 'fpStriked'
final_price_classname = 'fpPrice price'

soup = getSoupFromURL(url_search)

if soup:
    #share_content = soup.find_all(class_=classname)

    price_block = soup.find_all(class_= price_block_classname)
    print(price_block)


    striked_price = price_block.find_all(class_=striked_price_classname)
    #final_price = soup.find_all(class_=final_price_classname)
    #[0].text.strip()
    #print(striked_price)
    #print(final_price)
