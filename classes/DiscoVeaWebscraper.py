import time

from classes.BaseWebscraper import BaseWebscraper


class DiscoVeaWebscraper(BaseWebscraper):

    def __init__(self, url, keywords, name='Disco'):
        self.name = name
        self.products_prices = dict()
        super().__init__(url, keywords)
    
    def getProducts(self, waitingTime=2):
        """Returns a dictionary of product: price for every product listed on webpage
        """

        driver = self.getChromeDriver(incognito=True, headless=True)
        driver.get(self.url)
        time.sleep(waitingTime)
        
        # Find products and prices
        try:
            items_grid = driver.find_element_by_id('product-list')
            products_li = items_grid.find_elements_by_tag_name('li')
            self.products_prices = {
                self.getProduct(product): self.getFinalPrice(product) 
                    for product in products_li if self.keywords is None or any(kw.lower() in self.getProduct(product).lower() for kw in self.keywords)}
        except Exception as e:
            print(f'No results for given query. Error: {e}')
        
        # Close browser
        driver.quit()

        return self.products_prices

    def getProduct(self, element):
        return element.find_element_by_class_name('grilla-producto-descripcion').text.replace('\n', '').strip()

    def getFinalPrice(self, element):
        price = element.find_element_by_class_name('grilla-producto-precio').text.replace('$', '').strip()
        return f'$ {float(price):,.2f}'
