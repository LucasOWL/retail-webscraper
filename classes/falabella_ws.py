import time

from selenium.webdriver.common.keys import Keys

from classes.base_ws import BaseWS


class FalabellaWS(BaseWS):

    def __init__(self, url, keywords, name='Falabella'):
        self.name = name
        self.products_prices = dict()
        super().__init__(url, keywords)
    
    def get_products(self, waiting_time=2):
        """Returns a dictionary of product: price for every product listed on webpage
        """

        driver = self.get_chrome_driver(incognito=True, headless=True)
        driver.get(self.url)
        driver.find_element_by_xpath('//body').send_keys(Keys.END)  # scroll to bottom
        time.sleep(waiting_time)  # wait until everything is loaded
        
        # Find products and prices
        items_grid = driver.find_element_by_id('testId-searchResults-products')
        products_divs = items_grid.find_elements_by_xpath('.//div[contains(@class, "search-results")]')
        for product_div in products_divs:
            product = self.get_product(product_div)
            if self.keywords is None or self.any_keyword_is_present(product):
                self.products_prices.update({product: self.get_final_price(product_div)})
        
        # Close browser
        driver.quit()

        return self.products_prices

    def get_product(self, element):
        return element.find_element_by_xpath('.//b[contains(@class, "pod-subTitle")]').text.replace('\n', '').strip()

    def get_final_price(self, element):
        return element.find_element_by_xpath('.//li[contains(@class, "price-0")]/div/span').text.replace('Precio', '').strip()
    