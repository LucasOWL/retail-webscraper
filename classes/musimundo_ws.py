from classes.base_ws import BaseWS

class MusimundoWS(BaseWS):

    def __init__(self, url, keywords, name='Musimundo'):
        self.name = name
        self.products_prices = dict()
        super().__init__(url, keywords)

    def get_api_url(self, search, maxResults=100):
        return f'https://u.braindw.com/els/musimundoapi?ft={search}&qt={maxResults}&sc=emsa&refreshmetadata=true&exclusive=0&aggregations=true'

    def get_products(self, from_index=0, to_index=25):
        """Returns a dictionary of product: price for every product listed on webpage
        """

        search_terms = self.url.split('search?text=')[1]
        api_search_url = self.get_api_url(search=search_terms)
        items_info = self.download_content(api_search_url)

        if len(items_info) > 0:
            for item in items_info['hits']['hits']:
                product = self.get_product(item)
                if self.keywords is None or self.any_keyword_is_present(product):
                    if product not in self.products_prices:
                        self.products_prices.update({product: self.get_final_price(item)})
        
        return self.products_prices

    def get_product(self, item_info):
        return item_info['_source']['Descripcion'].strip()

    def get_final_price(self, item_info):
        return item_info['_source']['Precio']
