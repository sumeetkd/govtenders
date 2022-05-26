from .nicgepcrawler import NicgepCrawler

class nicgepcodeseproc:

    def __init__(self, name, base, url):
        self.name = name
        self.base = base
        self.url  = url
        self.crawler = NicgepCrawler(self.name, self.base, self.url)

    def crawler(self):
        return self.crawler