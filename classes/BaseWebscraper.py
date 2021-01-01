from urllib.request import urlopen
from bs4 import BeautifulSoup

class BaseWebscraper(object):
    
    def __init__(self, url, keywords=None):
        self.url = url
        self.keywords = keywords
    
    def __repr__(self):
        return f'{self.__class__.__name__}(url: {self.url}, keywords: {self.keywords})'
    
    def __str__(self):
        return f'{self.__class__.__name__}: {self.url} with keywords {self.keywords}'
