import time

from classes.base_ws import BaseWS


class DiscoVeaWS(BaseWS):

    def __init__(self, url, keywords, name='Disco'):
        self.name = name
        self.products_prices = dict()
        super().__init__(url, keywords)
    
    def get_products(self, waiting_time=2):
        """Returns a dictionary of product: price for every product listed on webpage
        """

        driver = self.get_chrome_driver(incognito=True, headless=True)
        driver.get(self.url)
        time.sleep(waiting_time)
        
        # Find products and prices
        items_grid = driver.find_element_by_id('product-list')
        products_li = items_grid.find_elements_by_tag_name('li')
        self.products_prices = {
            self.get_product(product): self.get_final_price(product) 
                for product in products_li if self.keywords is None or self.any_keyword_is_present(self.get_product(product))}
        
        # Close browser
        driver.quit()

        return self.products_prices

    def get_product(self, element):
        return element.find_element_by_class_name('grilla-producto-descripcion').text.replace('\n', '').strip()

    def get_final_price(self, element):
        price = element.find_element_by_class_name('grilla-producto-precio').text.replace('$', '').strip()
        return f'$ {float(price):,.2f}'
