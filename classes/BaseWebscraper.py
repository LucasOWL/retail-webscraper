import json
from concurrent.futures import ThreadPoolExecutor, wait
from urllib.request import urlopen

import requests
from bs4 import BeautifulSoup
from parameters import CHROMEDRIVER_PATH
from selenium import webdriver


class BaseWebscraper(object):
    
    NO_STOCK_STATUS = 'Sin stock'

    def __init__(self, url, keywords=None):
        self.url = url
        self.keywords = keywords
    
    def __repr__(self):
        return f'{self.__class__.__name__}(url: {self.url}, keywords: {self.keywords})'
    
    def __str__(self):
        return f'{self.__class__.__name__}: {self.url} with keywords {self.keywords}'
    
    def getChromeDriver(self, incognito=True, headless=True):
        """Initializes a Selenium webdriver Chrome instance
        """

        driver_options = webdriver.ChromeOptions()
        if incognito:
            driver_options.add_argument('--incognito')
        if headless:
            driver_options.add_argument('--headless')
        driver_options.add_experimental_option('excludeSwitches', ['enable-logging'])  # removes `DevTools listening on ...`
        driver = webdriver.Chrome(CHROMEDRIVER_PATH, options=driver_options)

        return driver
    
    def getPageSoup(self, url):
        """Returns webpage with BeautifulSoup
        """

        with urlopen(url) as uClient:
            page_html = uClient.read()
            page_soup = BeautifulSoup(page_html, 'html.parser')

        return page_soup
    
    def downloadContent(self, url):
        """Returns API response content
        """

        content = requests.get(url, stream=True)
        item_info = json.loads(content.text)

        return item_info
    
    # Multi threading requests
    def multiThreadDownloadContent(self, urls, maxWorkers=None):
        """Asynchronous execution of multiple url requests. Returns a list of Future` instances
        """

        with ThreadPoolExecutor(max_workers=maxWorkers) as executor:
            items_info = [executor.submit(self.downloadContent, url) for url in urls]
            wait(items_info)
        
        return items_info
