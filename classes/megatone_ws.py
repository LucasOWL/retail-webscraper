import time

from selenium.webdriver.common.keys import Keys

from classes.base_ws import BaseWS

class MegatoneWS(BaseWS):

    def __init__(self, url, keywords, name='Megatone'):
        self.name = name
        self.products_prices = dict()
        super().__init__(url, keywords)
    
    def get_products(self, waiting_time=2, page_number=1, driver=None):
        """Returns a dictionary of product: price for every product listed on webpage
        """
        
        page_number = page_number

        if driver is None:
            driver = self.get_chrome_driver(incognito=True, headless=True)
            driver.get(self.url)
            driver.find_element_by_xpath('//body').send_keys(Keys.END)  # scroll to bottom
            time.sleep(waiting_time)  # wait until everything is loaded
        
        # Find products and prices
        items_grid = driver.find_element_by_id('Productos')
        products_divs = items_grid.find_elements_by_class_name('CajaProductoGrilla')
        for product_div in products_divs:
            product = self.get_product(product_div)
            if self.keywords is None or self.any_keyword_is_present(product):
                self.products_prices.update({product: self.get_final_price(product_div)})
        
        # Recursively search in following pages
        page_number +=1
        try:
            next_page_button = driver.find_element_by_xpath(
                f'//button[@type="button" and contains(@class, "BtnPaginado") and text()={page_number}]')
            next_page_button.send_keys(Keys.ENTER)
            time.sleep(waiting_time)
            self.get_products(page_number=page_number, driver=driver)
        except:
            pass
        finally:
            # Close browser
            driver.quit()   
        
        return self.products_prices

    def get_product(self, element):
        return element.find_element_by_xpath('.//div[@class="aliLeft Titulo TituloMobile mL8"]').text.strip()

    def get_final_price(self, element):
        price =  element.find_element_by_xpath('.//div[contains(@class, "fLeft PrecioMostrado")]').text.replace('$', '').strip()
        return f'$ {float(price):,.2f}'
