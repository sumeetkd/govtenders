# This part has been written in order to handle the urls


class url_handler:

    def __init__(self,base):
        self.base = base

    def create_url(self, url):
        if url.find(self.base):
            result_url = (self.base+url)
        else:
            result_url = url
        return result_url
