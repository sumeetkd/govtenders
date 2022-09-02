from .nicgep import nicgepcodes
from .nicgepeproc import nicgepcodeseproc

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
			case 'Central_Institute_etenders':
				return nicgepcodes(self.name, self.base, self.url)
			case 'Manipur_Tenders':
				return nicgepcodeseproc(self.name, self.base, self.url)
			case 'Central_Institute_eprocure':
				return nicgepcodeseproc(self.name, self.base, self.url)
