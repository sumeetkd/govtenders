# This code should be able to handle the parsing of a standard National Informatics Centre based
# General Electronic Procurement websites. This includes a long list of websites which will need
# to be fed as the url to this function

from bs4 import BeautifulSoup
import re

class tender_item:


    def __init__(self, url, session):
        self.url = url
        self.session = session
        html_content = session.get(url).text
        print(html_content)
        self.soup = BeautifulSoup(html_content, 'html.parser')

    # Parsing of a standard tender item page to extract tender info. Any change in the website may force one to update this
    def tender_information(self):
        entry = {}
        for line in self.soup.find_all("table",class_="tablebg"):
            if not line.find_all("table",class_="list_table"):
                for caption,value in zip(line.find_all("td",class_='td_caption'),line.find_all("td",class_='td_field')):
                    dt = {caption.get_text().replace("\n","").replace("\t","").replace("\xa0","").replace("\r","") : value.get_text().replace("\n","").replace("\t","").replace("\xa0","").replace("\r","")}
                    entry.update(dt)
        return entry

    # Parsing of a standard tender item page to extract tender documents info. Any change in the website may force one to update this
    def tender_docs(self):
        listofvalues = []
        for item in self.soup.find_all("table", class_="list_table"):
            captions = []
            for line in item.find_all("tr", class_="list_header"):
                for caption in line.find_all("td"):
                    captions.append(caption.get_text().replace("\n", "").replace("\t", ""))
            for entry in item.find_all("tr", id=re.compile(r"\binformal_\w+")):
                values = []
                for field in entry.find_all("td"):
                    values.append(field.get_text().replace("\n", "").replace("\t", ""))
                    # print(values)
                if len(values)==len(captions):
                    compiled = dict(zip(captions, values))
                    listofvalues.append(compiled)
                else:
                    print("Captions and Values mismatch inside Table")
        return listofvalues