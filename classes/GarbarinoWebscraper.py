from classes.BaseWebscraper import BaseWebscraper

class GarbarinoWebscraper(BaseWebscraper):

    def __init__(self, url, keywords, name='Garbarino', products_prices={}):
        self.name = name
        self.products_prices = products_prices
        super().__init__(url, keywords)
    
    def getProducts(self):
        """Returns a dictionary of product: price for every product listed on webpage
        """
        
        page_soup = self.getPageSoup(self.url)
        # Find products and prices
        items_grid = page_soup.find('div', {'class': 'row itemList'})
        if items_grid is not None:
            products_divs = items_grid.find_all('div', recursive=False)
            for product_div in products_divs:
                product = self.getProduct(product_div)
                if self.keywords is None or any(kw.lower() in product.lower() for kw in self.keywords):
                    self.products_prices[product] = self.getFinalPrice(product_div)
        
        return self.products_prices

    def getProduct(self, bs4Element):
        return bs4Element.h3.text.strip().replace('*', '')

    def getFinalPrice(self, bs4Element):
        return bs4Element.find('span', {'class': 'value-item'}).text.strip()
