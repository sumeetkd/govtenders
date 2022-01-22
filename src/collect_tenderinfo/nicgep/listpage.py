from bs4 import BeautifulSoup
import re


class active_tender_page:

    def __init__(self, url, session):
        self.url = url
        self.session = session
        html_content = session.get(url).text
        self.soup = BeautifulSoup(html_content, 'html.parser')

    def extract_tender_item(self):
        for elem in self.soup.find_all("a", id=re.compile(r"\bDirectLin\w+")):
            yield elem.get('href')

    def next_page(self):
        nexturl = self.soup.find("a", id="linkFwd")
        if nexturl:
            result_url = nexturl.get('href')
        else:
            result_url = False
        return result_url