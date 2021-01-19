from classes.base_ws import BaseWS

class FravegaWS(BaseWS):

    def __init__(self, url, keywords, name='Frávega'):
        self.name = name
        self.products_prices = dict()
        super().__init__(url, keywords)
    
    def get_products(self):
        """Returns a dictionary of product: price for every product listed on webpage
        """
        
        page_soup = self.get_page_soup(self.url)
        # Find products and prices
        items_grid = page_soup.find('ul', {'name': 'itemsGrid'})
        if items_grid is not None:
            products_li = items_grid.find_all('li')
            self.products_prices = {
                self.get_product(product): self.get_final_price(product) 
                    for product in products_li if self.keywords is None or self.any_keyword_is_present(self.get_product(product))}

        return self.products_prices

    def get_product(self, bs4_element):
        return bs4_element.h4.text.strip()

    def get_final_price(self, bs4_element):
        return bs4_element.find('div', {'data-test-id': 'product-price'}).span.text.strip()
