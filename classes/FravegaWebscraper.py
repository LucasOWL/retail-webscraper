from classes.BaseWebscraper import BaseWebscraper

class FravegaWebscraper(BaseWebscraper):

    def __init__(self, url, keywords, name='Frávega'):
        self.name = name
        self.products_prices = dict()
        super().__init__(url, keywords)
    
    def getProducts(self):
        """Returns a dictionary of product: price for every product listed on webpage
        """
        
        page_soup = self.getPageSoup(self.url)
        # Find products and prices
        items_grid = page_soup.find('ul', {'name': 'itemsGrid'})
        if items_grid is not None:
            products_li = items_grid.find_all('li')
            self.products_prices = {
                self.getProduct(product): self.getFinalPrice(product) 
                    for product in products_li if self.keywords is None or any(kw.lower() in self.getProduct(product).lower() for kw in self.keywords)}

        return self.products_prices

    def getProduct(self, bs4Element):
        return bs4Element.h4.text.strip()

    def getFinalPrice(self, bs4Element):
        return bs4Element.find('div', {'data-test-id': 'product-price'}).span.text.strip()
