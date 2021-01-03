import os
import time
from classes.BaseWebscraper import BaseWebscraper
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
import json


class SonyWebscraper(BaseWebscraper):

    CHROMEDRIVER_PATH = os.path.join(r'C:\webdrivers\chromedriver.exe')
    SONY_API_BASE_URL = 'https://store.sony.com.ar/api/catalog_system/pub/products/variations/'
    
    def getItemsIds(self, waitingTime=5):
        """Scraps Sony`s URL and gets every data-id for every product listed
        """

        # Configure driver
        driver_options = webdriver.ChromeOptions()
        driver_options.add_argument('--incognito')
        driver_options.add_argument('--headless')
        driver_options.add_argument("--log-level=3")
        driver = webdriver.Chrome(self.CHROMEDRIVER_PATH, options=driver_options)

        # Get page
        driver.get(self.url)
        driver.find_element_by_xpath('//body').send_keys(Keys.END)  # scroll to bottom
        time.sleep(waitingTime)  # wait until everything is loaded
        
        # Get items
        items_grid =  driver.find_element_by_xpath('//div[@class="vitrine resultItemsWrapper"]//div[@class="items"]')
        items_pages = items_grid.find_elements_by_xpath(
            '//div[contains(@class, "items") and contains(@class, "colunas") and contains(@class, "fixed")]')

        items_ids = set() 
        for items_page in items_pages:
            div_elements = items_page.find_elements_by_tag_name('div')
            items_ids.update([div.get_attribute('data-id') for div in div_elements if div.get_attribute('data-id') is not None])
        
        # Close browser
        driver.quit()
        
        return items_ids
    
    def getProducts(self):
        """Returns a dictionary of product: price for every product listed on webpage
        """

        items_ids = self.getItemsIds(waitingTime=5)
        products_prices = {}
        for item_id in items_ids:
            item_api_url = f'{self.SONY_API_BASE_URL}{item_id}'
            content = requests.get(item_api_url)
            item_info = json.loads(content.text)
            product = self.getProduct(item_info)
            if self.keywords is None or any(kw.lower() in product.lower() for kw in self.keywords):
                products_prices.update({product: self.getFinalPrice(item_info)})
        
        return products_prices

    def getProduct(self, itemInfo):
        return itemInfo['name'].strip()

    def getFinalPrice(self, itemInfo):
        if itemInfo['available']:
            return itemInfo['skus'][0]['bestPriceFormated'].strip()
        else:
            return self.NO_STOCK_STATUS
