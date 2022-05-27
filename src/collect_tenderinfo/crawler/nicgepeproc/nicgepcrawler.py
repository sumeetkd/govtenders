import requests
from requests.exceptions import ConnectionError
import re
import time
import random
import numpy
from bs4 import BeautifulSoup
from .nicgepparser import NicgepParser

def get_random_ua():
	random_ua = ''
	ua_file = 'src/collect_tenderinfo/crawler/nicgepeproc/ua_file.txt'
	try:
		with open(ua_file) as f:
			lines = f.readlines()
		if len(lines) > 0:
			prng = numpy.random.RandomState()
			index = prng.permutation(len(lines) - 1)
			idx = numpy.asarray(index, dtype=numpy.integer)[0]
			random_ua = lines[int(idx)]
	except Exception as ex:
		print('Exception in random_ua')
		print(str(ex))
	finally:
		return random_ua

#headers = {
#
#	'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0'
#}

class websessions:

	def __init__(self):
		self.s = None

	def __enter__(self):
		self.s = requests.session()
		self.s.headers.update(headers)
		return self.s

	def __exit__(self, exc_type, exc_val, exc_tb):
		self.s.end_headers()


class NicgepCrawler:
	"""
	At this point we have started the session that is kept alive till we finish crawling on this website

	"""
	def __init__(self, name, base, url):
		self.name = name
		self.base = base
		self.url = self.create_url(url)
		self.s = None
		self.ua= ''

	def get_ua(self):
		user_agent = get_random_ua()
		return user_agent.replace("\n","")

	def orgnumbers(self):
		org_html = requests.get(self.url).text
		soup = BeautifulSoup(org_html, 'html.parser')
		orgnolist = []
		for row in soup.find_all("tr", id=re.compile("informal")):
			srno = int(row.contents[1].string)
			nooftenders = int(row.find("a").get_text())
			orgnolist.append((srno, nooftenders))
		#print(orgnolist)
		return orgnolist

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
		
		orgnumbers = self.orgnumbers()
		for i in range(len(orgnumbers)):
			for j in range(orgnumbers[i][1]):
				self.ua = self.get_ua()
				headers = {
						'user-agent': self.ua, 
					}
				counter = 0
				while counter < 30:
					try:
						with requests.session() as self.s:
							org_html = self.s.get(self.url, headers=headers).text
							soup = BeautifulSoup(org_html, 'html.parser')
							for row in soup.find_all("tr", id=re.compile("informal")):
								if int(row.contents[1].string) == i+1:
									orgpages = row.find("a", id=re.compile(r"\bDirectLin\w+")).get('href')
									orgpage_html = self.s.get(self.create_url(orgpages), headers=headers).text
									orgsoup = BeautifulSoup(orgpage_html, 'html.parser')
									for item in orgsoup.find_all("tr", id=re.compile("informal")):
										if int(item.contents[1].string) == j+1:
											tenderinfourl = self.create_url(item.find("a", id=re.compile(r"\bDirectLin\w+")).get('href'))
											tenderinfo = self.s.get(tenderinfourl, headers=headers).text
											infosoup = BeautifulSoup(tenderinfo, 'html.parser')
											yield infosoup
						counter = 31
					except ConnectionError:
						print("Connection Error...")
						time.sleep(120)
						counter += 1

	def tenderpage_parser(self, infosoup):
		entry = {}
		for line in infosoup.find_all("table", class_="tablebg"):
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
