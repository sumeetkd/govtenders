import requests, time, re
from random import randint
from nicgep import url_handler
from nicgep import active_tender_page
from nicgep import tender_item
from data import data_entry
from bs4 import BeautifulSoup
import json
import pandas as pd

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}
#name = 'Manipur'
#base = 'https://manipurtenders.gov.in/'
## base = 'https://etenders.gov.in'
## url_at_base = '/eprocure/app?page=FrontEndLatestActiveTenders&service=page'
#
#url = 'nicgep/app?page=FrontEndLatestActiveTenders&service=page'
#u = url_handler(base)
#data = data_entry(name, base)

class tender_site:

    def __init__(self,name,base,url):
        self.name = name
        self.base = base
        self.url  = url
        self.data = data_entry(name)
        self.u    = url_handler(base)


    def collect_page(self):
        """

        :return:
        """
        tender_items = []
        url_post = self.url
        org_html = requests.get(self.url).text
        soup = BeautifulSoup(org_html, 'html.parser')
        for elem in soup.find_all("a", id=re.compile(r"\bDirectLin\w+")):
            s = requests.session()
            s.headers.update(headers)
            url = self.u.create_url(elem.get('href'))
            list_page = active_tender_page(url,s)
            Unique = True
            while Unique:
                for item in list_page.extract_tender_item():
#                    time.sleep(randint(0,3))
                    item_url = self.u.create_url(item)
                    item_page = tender_item(item_url,s)
                    entry = item_page.tender_information()
                    Unique = self.data.check_unique(entry) and (not (entry in tender_items))
                    if Unique:
                        tender_items.append(entry)
            print("End for Organization")
#            if Unique:
#                url_post = list_page.next_page()
#            else:
#                url_post = False
        self.data.save_data(tender_items)
        return print(self.name,'Completed')


if __name__ == "__main__":
    """
    Collect tender website url
    """
    tender_sites = 'src/collect_tenderinfo/tender_sites.json'
    with open(tender_sites, 'r') as jsonfile:
        tendersites_info = json.load(jsonfile)
        for item in tendersites_info:
            site = tender_site(item['name'],item['base'],item['url'])
            site.collect_page()
