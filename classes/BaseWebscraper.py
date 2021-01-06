from selenium import webdriver
from parameters import CHROMEDRIVER_PATH

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
