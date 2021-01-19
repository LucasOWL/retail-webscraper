from classes.base_ws import BaseWS

class GarbarinoCompumundoWS(BaseWS):

    def __init__(self, url, keywords, name='Garbarino'):
        self.name = name
        self.products_prices = dict()
        super().__init__(url, keywords)
    
    def get_products(self):
        """Returns a dictionary of product: price for every product listed on webpage
        """
        
        page_soup = self.get_page_soup(self.url)
        # Find products and prices
        items_grid = page_soup.find('div', {'class': 'row itemList'})
        if items_grid is not None:
            products_divs = items_grid.find_all('div', recursive=False)
            for product_div in products_divs:
                product = self.get_product(product_div)
                if self.keywords is None or self.any_keyword_is_present(product):
                    self.products_prices[product] = self.get_final_price(product_div)
        
        return self.products_prices

    def get_product(self, bs4_element):
        return bs4_element.h3.text.strip().replace('*', '')

    def get_final_price(self, bs4_element):
        return bs4_element.find('span', {'class': 'value-item'}).text.strip()
