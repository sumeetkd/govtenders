from .nicgep import nicgepcodes

class choose_site_class:
	"""
	Choosing the website crawling mechanism and the parser
	"""
	def __init__(self,name,base,url):
		self.name = name
		self.base = base
		self.url  = url

	def load(self):
		match self.name:
			case 'Central website':
				return nicgepcodes(self.name, self.base, self.url)
			case 'Manipur Tenders':
				return nicgepcodes(self.name, self.base, self.url)
			case _:
				return nicgepcodes(self.name, self.base, self.url)
