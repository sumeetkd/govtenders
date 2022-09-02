import time

from crawler import choose_site_class
import json
import src.sqlconnection


sqlconnection = src.sqlconnection.connector
sqlupdater = src.sqlconnection.sqlupdater

if __name__ == "__main__":
	"""
	Running it all together
      - Collect the names and urls of the websites from json file
      - For each item in this list pull out the data from the website parse the data extracted
      - Save the data into a database
	"""
	# [TODO] Pass into config file
	tender_sites = 'src/collect_tenderinfo/tender_sites.json'
	with open(tender_sites, 'r') as jsonfile:
		tendersites_info = json.load(jsonfile)
		for item in tendersites_info:
			with sqlconnection() as connection:
				print("Start of Website")
				writer = sqlupdater(connection)
				website = choose_site_class(item['name'],item['base'],item['url']).load()
				for page in website.crawler.tenderpage_url_generator():
					entry = website.crawler.tenderpage_parser(page)
#			print(entry)
					writer.insertsql(entry)
				writer.updatedb()
				print("End for Website")
		print("End for all Tenders")
