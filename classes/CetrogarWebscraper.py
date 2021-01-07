from classes.BaseWebscraper import BaseWebscraper

class CetrogarWebscraper(BaseWebscraper):

    def __init__(self, url, keywords, name='Cetrogar', products_prices={}):
        self.name = name
        self.products_prices = products_prices
        super().__init__(url, keywords)
    
    def getProducts(self):
        """Returns a dictionary of product: price for every product listed on webpage
        """

        page_soup = self.getPageSoup(self.url)
        # Find products and prices
        items_grid = page_soup.find('div', {'class': 'products wrapper grid products-grid'})
        if items_grid is not None:
            products_li = items_grid.find_all('li')
            self.products_prices = {
                self.getProduct(product): self.getFinalPrice(product) 
                    for product in products_li if self.keywords is None or any(kw.lower() in self.getProduct(product).lower() for kw in self.keywords)}

        return self.products_prices

    def getProduct(self, bs4Element):
        return bs4Element.find('a', {'class': 'product-item-link'}).text.replace('\n', '').strip()

    def getFinalPrice(self, bs4Element):
        return bs4Element.find('span', {'data-price-type': 'finalPrice'}).find('span', {'class': 'price'}).text.strip()
