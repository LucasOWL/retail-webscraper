import time

from selenium.webdriver.common.keys import Keys

from classes.base_ws import BaseWS

class CarrefourWS(BaseWS):

    def __init__(self, url, keywords, name='Carrefour'):
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
        try:
            items_grid = driver.find_element_by_xpath(
                '//div[@class="category-products"]//div[@class="row"]')
            products_divs = items_grid.find_elements_by_xpath(
                './/div[contains(@class, "col") and contains(@class, "product-card")]')
            for product_div in products_divs:
                product = self.get_product(product_div)
                if self.keywords is None or self.any_keyword_is_present(product):
                    self.products_prices.update({product: self.get_final_price(product_div)})
        except:
            pass
        
        # Close browser
        driver.quit()
        
        return self.products_prices

    def get_product(self, element):
        return element.find_element_by_class_name('title').text.strip()

    def get_final_price(self, element):
        return element.find_element_by_xpath('.//p[@class="price"]').text.strip().replace('\n', '')
