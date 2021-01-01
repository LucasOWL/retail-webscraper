from urllib.request import urlopen
from bs4 import BeautifulSoup
from classes.BaseWebscraper import BaseWebscraper

class FravegaWebscraper(BaseWebscraper):
    
    def checkProducts(self):
        """Returns a dictionary of product: price for every product listed on webpage
        """
        
        uClient = urlopen(self.url)
        page_html = uClient.read()
        page_soup = BeautifulSoup(page_html, 'html.parser')
        
        products_prices = {'': ''}
        # Find products and prices
        items_grid = page_soup.find('ul', {'name': 'itemsGrid'})
        if items_grid is not None:
            products_li = items_grid.find_all('li')
            products_prices = {
                self.getProduct(product): self.getFinalPrice(product) 
                    for product in products_li if self.keywords is None or any(kw.lower() in self.getProduct(product).lower() for kw in self.keywords)}
        uClient.close()

        return products_prices

    def getProduct(self, bs4Element):
        return bs4Element.h4.text.strip()

    def getFinalPrice(self, bs4Element):
        return bs4Element.find('div', {'data-test-id': 'product-price'}).span.text.strip()
