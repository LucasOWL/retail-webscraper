import time

from selenium.webdriver.common.keys import Keys

from classes.BaseWebscraper import BaseWebscraper

class MegatoneWebscraper(BaseWebscraper):

    def __init__(self, url, keywords, name='Megatone'):
        self.name = name
        self.products_prices = dict()
        super().__init__(url, keywords)
    
    def getProducts(self, waitingTime=2, pageNumber=1, driver=None):
        """Returns a dictionary of product: price for every product listed on webpage
        """
        
        page_number = pageNumber

        if driver is None:
            driver = self.getChromeDriver(incognito=True, headless=True)
            driver.get(self.url)
            driver.find_element_by_xpath('//body').send_keys(Keys.END)  # scroll to bottom
            time.sleep(waitingTime)  # wait until everything is loaded
        
        # Find products and prices
        try:
            items_grid = driver.find_element_by_id('Productos')
            products_divs = items_grid.find_elements_by_class_name('CajaProductoGrilla')
            for product_div in products_divs:
                product = self.getProduct(product_div)
                if self.keywords is None or self.anyKeywordIsPresent(product):
                    self.products_prices.update({product: self.getFinalPrice(product_div)})
        except Exception as e:
            print(f'No results for given query. Error: {e}')
        
        # Recursively search in following pages
        page_number +=1
        try:
            next_page_button = driver.find_element_by_xpath(
                f'//button[@type="button" and contains(@class, "BtnPaginado") and text()={page_number}]')
            next_page_button.send_keys(Keys.ENTER)
            time.sleep(waitingTime)
            self.getProducts(pageNumber=page_number, driver=driver)
        except:
            pass
        finally:
            # Close browser
            driver.quit()   
        
        return self.products_prices

    def getProduct(self, element):
        return element.find_element_by_xpath('.//div[@class="aliLeft Titulo TituloMobile mL8"]').text.strip()

    def getFinalPrice(self, element):
        price =  element.find_element_by_xpath('.//div[contains(@class, "fLeft PrecioMostrado")]').text.replace('$', '').strip()
        return f'$ {float(price):,.2f}'
