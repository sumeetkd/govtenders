import requests
import re
from bs4 import BeautifulSoup
from .nicgepparser import NicgepParser

headers = {
	'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
	AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}


class NicgepCrawler:
	"""
	At this point we have started the session that is kept alive till we finish crawling on this website

	"""
	def __init__(self, name, base, url):
		self.name = name
		self.base = base
		self.url = self.create_url(url)
		self.s = None

	def org_list_wrangler(self, url):
		html_content = requests.get(url).text
		soup = BeautifulSoup(html_content, 'html.parser')
		for elem in soup.find_all("a", id=re.compile(r"\bDirectLin\w+")):
			yield self.create_url(elem.get('href'))

	def list_page_wrangler(self, url):
		html_content = self.s.get(url).text
		soup = BeautifulSoup(html_content, 'html.parser')
		for elem in soup.find_all("a", id=re.compile(r"\bDirectLin\w+")):
			yield self.create_url(elem.get('href'))

	def tenderpage_url_generator(self):
		for orgpages in self.org_list_wrangler(self.url):
			with requests.session() as self.s:
				self.s.headers.update(headers)
				for item in self.list_page_wrangler(orgpages):
					yield item

	def tenderpage_parser(self, url):
		entry = {}
		html_content = self.s.get(url).text
		soup = BeautifulSoup(html_content, 'html.parser')
		for line in soup.find_all("table", class_="tablebg"):
			if not line.find_all("table", class_="list_table"):
				for caption, value in zip(line.find_all("td", class_='td_caption'), line.find_all("td", class_='td_field')):
					dt = {caption.get_text().replace("\n", "").replace("\t", "").replace("\xa0", "").replace("\r", ""):
							value.get_text().replace("\n", "").replace("\t", "").replace("\xa0", "").replace("\r", "")}
					entry.update(dt)
		return NicgepParser(self.name, self.base, entry).parsed_sql_entry()

	def create_url(self, url):
		if url.find(self.base):
			return self.base+url
		else:
			return url
