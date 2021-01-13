from classes.BaseWebscraper import BaseWebscraper

class MusimundoWebscraper(BaseWebscraper):

    def __init__(self, url, keywords, name='Musimundo'):
        self.name = name
        self.products_prices = dict()
        super().__init__(url, keywords)

    def getAPIUrl(self, search, maxResults=100):
        return f'https://u.braindw.com/els/musimundoapi?ft={search}&qt={maxResults}&sc=emsa&refreshmetadata=true&exclusive=0&aggregations=true'

    def getProducts(self, fromIndex=0, toIndex=25):
        """Returns a dictionary of product: price for every product listed on webpage
        """

        search_terms = self.url.split('search?text=')[1]
        api_search_url = self.getAPIUrl(search=search_terms)
        items_info = self.downloadContent(api_search_url)

        if len(items_info) > 0:
            for item in items_info['hits']['hits']:
                product = self.getProduct(item)
                if self.keywords is None or self.anyKeywordIsPresent(product):
                    if product not in self.products_prices:
                        self.products_prices.update({product: self.getFinalPrice(item)})
        
        return self.products_prices

    def getProduct(self, itemInfo):
        return itemInfo['_source']['Descripcion'].strip()

    def getFinalPrice(self, itemInfo):
        return itemInfo['_source']['Precio']
