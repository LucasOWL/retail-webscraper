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
            for product_li in products_li:
                product = self.get_product(product_li)
                if product is not None and (self.keywords is None or self.any_keyword_is_present(product)):
                    self.products_prices[product] = self.get_final_price(product_li)

        return self.products_prices

    def get_product(self, bs4_element):
        product = bs4_element.h4
        if product is not None:
            product = product.text.strip()
        return product

    def get_final_price(self, bs4_element):
        return bs4_element.find('div', {'data-test-id': 'product-price'}).span.text.strip()
