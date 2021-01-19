from classes.base_ws import BaseWS

class CetrogarWS(BaseWS):

    def __init__(self, url, keywords, name='Cetrogar'):
        self.name = name
        self.products_prices = dict()
        super().__init__(url, keywords)
    
    def get_products(self):
        """Returns a dictionary of product: price for every product listed on webpage
        """

        page_soup = self.get_page_soup(self.url)
        # Find products and prices
        items_grid = page_soup.find('div', {'class': 'products wrapper grid products-grid'})
        if items_grid is not None:
            products_li = items_grid.find_all('li')
            self.products_prices = {
                self.get_product(product): self.get_final_price(product) 
                    for product in products_li if self.keywords is None or self.any_keyword_is_present(self.get_product(product))}

        return self.products_prices

    def get_product(self, bs4_element):
        return bs4_element.find('a', {'class': 'product-item-link'}).text.replace('\n', '').strip()

    def get_final_price(self, bs4_element):
        return bs4_element.find('span', {'data-price-type': 'finalPrice'}).find('span', {'class': 'price'}).text.strip()
