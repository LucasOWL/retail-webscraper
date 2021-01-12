import time

from selenium.webdriver.common.keys import Keys

from classes.BaseWebscraper import BaseWebscraper


class SonyWebscraper(BaseWebscraper):

    API_BASE_URL = 'https://store.sony.com.ar/api/catalog_system/pub/products/variations/'
    
    def __init__(self, url, keywords, name='Sony', products_prices={}):
        self.name = name
        self.products_prices = products_prices
        super().__init__(url, keywords)
        
    def getItemsIds(self, waitingTime=5):
        """Scraps Sony`s URL and gets every data-id for every product listed
        """

        # Get page
        driver = self.getChromeDriver(incognito=True, headless=True)
        driver.get(self.url)
        driver.find_element_by_xpath('//body').send_keys(Keys.END)  # scroll to bottom
        time.sleep(waitingTime)  # wait until everything is loaded
        
        items_ids = set()
        try:
            # Get items
            items_grid =  driver.find_element_by_xpath('//div[@class="vitrine resultItemsWrapper"]//div[@class="items"]')
            items_pages = items_grid.find_elements_by_xpath(
                '//div[contains(@class, "items") and contains(@class, "colunas") and contains(@class, "fixed")]')

            for items_page in items_pages:
                div_elements = items_page.find_elements_by_tag_name('div')
                items_ids.update([div.get_attribute('data-id') for div in div_elements if div.get_attribute('data-id') is not None])
        except Exception as e:
            print(f'No results for given query. Error: {e}')

        # Close browser
        driver.quit()
        
        return items_ids
    
    def getProducts(self):
        """Returns a dictionary of product: price for every product listed on webpage
        """

        items_ids = self.getItemsIds(waitingTime=5)
        api_urls = [f'{self.API_BASE_URL}{item_id}' for item_id in items_ids]
        items_info = self.multiThreadDownloadContent(api_urls)
        
        for item_info in items_info:
            item_info_dict = item_info.result()
            product = self.getProduct(item_info_dict)
            if self.keywords is None or any(kw.lower() in product.lower() for kw in self.keywords):
                self.products_prices.update({product: self.getFinalPrice(item_info_dict)})
        
        return self.products_prices
    
    def getProduct(self, itemInfo):
        return itemInfo['name'].strip()

    def getFinalPrice(self, itemInfo):
        if itemInfo['available']:
            return itemInfo['skus'][0]['bestPriceFormated'].strip()
        else:
            return self.NO_STOCK_STATUS
