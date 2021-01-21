import json
from concurrent.futures import ThreadPoolExecutor, wait
from urllib.request import Request, urlopen

import requests
from bs4 import BeautifulSoup
from selenium import webdriver


class BaseWS(object):
    
    NO_STOCK_STATUS = 'Out of stock'
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36'
    }

    def __init__(self, url, keywords=None):
        self.url = url
        self.keywords = keywords
    
    def __repr__(self):
        return f'{self.__class__.__name__}(url: {self.url}, keywords: {self.keywords})'
    
    def __str__(self):
        return f'{self.__class__.__name__}: {self.url} with keywords {self.keywords}'
    
    def get_chrome_driver(self, incognito=True, headless=True):
        """Initializes a Selenium webdriver Chrome instance
        """

        with open('config.json', encoding='utf-8') as f:
            params = json.load(f)
            chromedriver_path = params['CHROMEDRIVER_PATH']
        
        driver_options = webdriver.ChromeOptions()
        if incognito:
            driver_options.add_argument('--incognito')
        if headless:
            driver_options.add_argument('--headless')
        driver_options.add_experimental_option('excludeSwitches', ['enable-logging'])  # removes `DevTools listening on ...`
        driver = webdriver.Chrome(chromedriver_path, options=driver_options)

        return driver
    
    
    def get_content(self, url):
        """Returns URL content from request
        """

        session = requests.Session()
        content = session.get(url, headers=self.HEADERS, stream=True).text
        session.close()

        return content
    
    def get_page_soup(self, url):
        """Returns webpage with BeautifulSoup
        """

        content = self.get_content(url)
        page_soup = BeautifulSoup(content, 'html.parser')

        return page_soup
    
    def get_content_json(self, url):
        """Returns webpage as json
        """

        content = self.get_content(url)
        item_info = json.loads(content)
        
        return item_info
    
    # Multi threaded requests
    def multithread_get_content_json(self, urls, max_workers=None):
        """Asynchronous execution of multiple url requests. Returns a list of Future`s instances
        """

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            items_info = [executor.submit(self.get_content_json, url) for url in urls]
            wait(items_info)
        
        return items_info
    
    def any_keyword_is_present(self, product):
        return any(kw.lower() in product.lower().strip() for kw in self.keywords)
