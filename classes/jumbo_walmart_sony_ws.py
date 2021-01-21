from classes.base_ws import BaseWS


class JumboWalmartSonyWS(BaseWS):

    MAX_API_RESULTS = 26

    def __init__(self, url, keywords, name='Jumbo'):
        self.name = name
        self.products_prices = dict()
        super().__init__(url, keywords)

    def get_api_url(self, search, from_index=0, to_index=25):
        if self.name == 'Jumbo':
            return f'https://www.jumbo.com.ar/api/catalog_system/pub/products/search/?&&ft={search}&O=OrderByScoreDESC&_from={from_index}&_to={to_index}'
        elif self.name == 'Walmart':
            return f'https://www.walmart.com.ar/api/catalog_system/pub/products/search/?&cc=50&PageNumber=1&sm=0&ft={search}&sc=15&_from={from_index}&_to={to_index}'
        elif self.name == 'Sony':
            return f'https://store.sony.com.ar/api/catalog_system/pub/products/search/?&ft={search}&_from={from_index}&_to={to_index}'

    def get_products(self, from_index=0, to_index=25):
        """Returns a dictionary of product: price for every product listed on webpage
        """

        if '?ft=' in self.url:
            search_terms = self.url.split('?ft=')[1]
        elif 'text=' in self.url:
            search_terms = self.url.split('text=')[1]
        else:
            search_terms = self.url.split('.ar/')[1]

        from_index = from_index
        to_index = to_index
        api_search_url = self.get_api_url(search=search_terms, from_index=from_index, to_index=to_index)
        items_info = self.get_content_json(api_search_url)

        if len(items_info) > 0:
            for item in items_info:
                product = self.get_product(item)
                if self.keywords is None or self.any_keyword_is_present(product):
                    if product not in self.products_prices:
                        self.products_prices.update({product: self.get_final_price(item)})
        
        # Recursively scan following pages
        if len(items_info) == self.MAX_API_RESULTS:
            from_index = to_index + 1
            to_index += self.MAX_API_RESULTS
            self.get_products(from_index=from_index, to_index=to_index)
        
        return self.products_prices

    def get_product(self, item_info):
        return item_info['productName'].strip()

    def get_final_price(self, item_info):
        commertial_offer = item_info['items'][0]['sellers'][0]['commertialOffer']
        if self.get_available_quantity(commertial_offer) == 0:
            return self.NO_STOCK_STATUS
        else:
            price = commertial_offer['Price']
            return f'$ {price:,.2f}'
    
    def get_available_quantity(self, commertial_offer):
        return commertial_offer['AvailableQuantity']
