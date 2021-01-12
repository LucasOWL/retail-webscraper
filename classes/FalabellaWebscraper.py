import time

from selenium.webdriver.common.keys import Keys

from classes.BaseWebscraper import BaseWebscraper


class FalabellaWebscraper(BaseWebscraper):

    def __init__(self, url, keywords, name='Falabella'):
        self.name = name
        self.products_prices = dict()
        super().__init__(url, keywords)
    
    def getProducts(self, waitingTime=2):
        """Returns a dictionary of product: price for every product listed on webpage
        """

        driver = self.getChromeDriver(incognito=True, headless=True)
        driver.get(self.url)
        driver.find_element_by_xpath('//body').send_keys(Keys.END)  # scroll to bottom
        time.sleep(waitingTime)  # wait until everything is loaded
        
        # Find products and prices
        try:
            items_grid = driver.find_element_by_id('testId-searchResults-products')
            products_divs = items_grid.find_elements_by_xpath('//div[contains(@class, "search-results-4-grid grid-pod")]')
            for product_div in products_divs:
                product = self.getProduct(product_div)
                if self.keywords is None or any(kw.lower() in product.lower() for kw in self.keywords):
                    self.products_prices.update({product: self.getFinalPrice(product_div)})
        except Exception as e:
            print(f'No results for given query. Error: {e}')
        
        # Close browser
        driver.quit()

        return self.products_prices

    def getProduct(self, element):
        return element.find_element_by_xpath('.//b[contains(@class, "pod-subTitle")]').text.replace('\n', '').strip()

    def getFinalPrice(self, element):
        return element.find_element_by_xpath('.//li[contains(@class, "price-0")]/div/span').text.replace('Precio', '').strip()
    