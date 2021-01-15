from classes.BaseWebscraper import BaseWebscraper


class JumboWalmartSonyWebscraper(BaseWebscraper):

    MAX_API_RESULTS = 26

    def __init__(self, url, keywords, name='Jumbo'):
        self.name = name
        self.products_prices = dict()
        super().__init__(url, keywords)

    def getAPIUrl(self, search, fromIndex=0, toIndex=25):
        if self.name == 'Jumbo':
            return f'https://www.jumbo.com.ar/api/catalog_system/pub/products/search/?&&ft={search}&O=OrderByScoreDESC&_from={fromIndex}&_to={toIndex}'
        elif self.name == 'Walmart':
            return f'https://www.walmart.com.ar/api/catalog_system/pub/products/search/?&cc=50&PageNumber=1&sm=0&ft={search}&sc=15&_from={fromIndex}&_to={toIndex}'
        elif self.name == 'Sony':
            return f'https://store.sony.com.ar/api/catalog_system/pub/products/search/?&ft={search}&_from={fromIndex}&_to={toIndex}'

    def getProducts(self, fromIndex=0, toIndex=25):
        """Returns a dictionary of product: price for every product listed on webpage
        """

        if '?ft=' in self.url:
            search_terms = self.url.split('?ft=')[1]
        elif 'text=' in self.url:
            search_terms = self.url.split('text=')[1]
        else:
            search_terms = self.url.split('.ar/')[1]

        from_index = fromIndex
        to_index = toIndex
        api_search_url = self.getAPIUrl(search=search_terms, fromIndex=from_index, toIndex=to_index)
        items_info = self.downloadContent(api_search_url)

        if len(items_info) > 0:
            for item in items_info:
                product = self.getProduct(item)
                if self.keywords is None or self.anyKeywordIsPresent(product):
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
        commertial_offer = itemInfo['items'][0]['sellers'][0]['commertialOffer']
        if self.getAvailableQuantity(commertial_offer) == 0:
            return self.NO_STOCK_STATUS
        else:
            price = commertial_offer['Price']
            return f'$ {price:,.2f}'
    
    def getAvailableQuantity(self, commertialOffer):
        return commertialOffer['AvailableQuantity']
