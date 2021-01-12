from classes.BaseWebscraper import BaseWebscraper


class JumboWebscraper(BaseWebscraper):

    MAX_API_RESULTS = 26

    def __init__(self, url, keywords, name='Jumbo', products_prices={}):
        self.name = name
        self.products_prices = products_prices
        super().__init__(url, keywords)

    def getAPIUrl(self, search, fromIndex=0, toIndex=25):
        return f'https://www.jumbo.com.ar/api/catalog_system/pub/products/search/?&&ft={search}&O=OrderByScoreDESC&_from={fromIndex}&_to={toIndex}'

    def getProducts(self, fromIndex=0, toIndex=25):
        """Returns a dictionary of product: price for every product listed on webpage
        """

        search_terms = self.url.split('?ft=')[1]

        from_index = fromIndex
        to_index = toIndex
        api_search_url = self.getAPIUrl(search=search_terms, fromIndex=from_index, toIndex=to_index)
        items_info = self.downloadContent(api_search_url)

        if len(items_info) > 0:
            for item in items_info:
                product = self.getProduct(item)
                if self.keywords is None or any(kw.lower() in product.lower() for kw in self.keywords):
                    if product not in self.products_prices:
                        self.products_prices.update({product: self.getFinalPrice(item)})
        
        # Recursively scan following pages
        if len(items_info) == self.MAX_API_RESULTS:
            from_index = to_index + 1
            to_index += self.MAX_API_RESULTS
            self.getProducts(fromIndex=from_index, toIndex=to_index)
        
        return self.products_prices

    def getProduct(self, itemInfo):
        return itemInfo['productName'].strip()

    def getFinalPrice(self, itemInfo):
        price = itemInfo['items'][0]['sellers'][0]['commertialOffer']['Price']
        return f'$ {price:,.2f}'
