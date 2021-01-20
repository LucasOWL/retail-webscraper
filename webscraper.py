import json
import smtplib
import time
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from secrets import password, to_address, username

from colorama import Fore, Style, init

from classes.base_ws import BaseWS
from classes.cetrogar_ws import CetrogarWS
from classes.disco_vea_ws import DiscoVeaWS
from classes.falabella_ws import FalabellaWS
from classes.fravega_ws import FravegaWS
from classes.garbarino_compumundo_ws import GarbarinoCompumundoWS
from classes.jumbo_walmart_sony_ws import JumboWalmartSonyWS
from classes.musimundo_ws import MusimundoWS
from classes.carrefour_ws import CarrefourWS
from classes.megatone_ws import MegatoneWS

class Webscraper(object):

    NO_STOCK_STATUS = BaseWS.NO_STOCK_STATUS
            
    def __init__(self, urls_keywords_dict, email_subject, username, password, to_address, timeout):
        self.urls_keywords_dict = urls_keywords_dict
        self.email_subject = email_subject
        self.username = username
        self.password = password
        self.to_address = to_address
        self.timeout = timeout

        self.webpage_to_object = {
            'Frávega': FravegaWS,
            'Cetrogar': CetrogarWS,
            'Sony': JumboWalmartSonyWS,
            'Jumbo': JumboWalmartSonyWS,
            'Disco': DiscoVeaWS,
            'Vea Digital': DiscoVeaWS,
            'Falabella': FalabellaWS,
            'Walmart': JumboWalmartSonyWS,
            'Garbarino': GarbarinoCompumundoWS,
            'Musimundo': MusimundoWS,
            'Compumundo': GarbarinoCompumundoWS,
            'Carrefour': CarrefourWS,
            'Megatone': MegatoneWS,
        }
    
    def __repr__(self):
        return f'{self.__class__.__name__}({self.urls_keywords_dict})'
    
    def __str__(self):
        return f'{self.__class__.__name__}: {self.urls_keywords_dict}'
    
    def get_url(self, webpage):
        """Returns URL from parameters file
        """

        try:
            return self.urls_keywords_dict[webpage]['URL']
        except:
            return None
    
    def get_keywords(self, webpage):
        """Returns keywords from parameters file
        """
        
        try:
            return self.urls_keywords_dict[webpage]['keywords']
        except:
            return None
    
    def get_url_keywords(self, webpage):
        """Returns dictionary with url, keywords and name for webpage constructor
        """

        return {'url': self.get_url(webpage), 'keywords': self.get_keywords(webpage), 'name': webpage}
    
    def get_current_time(self):
        return datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    def get_all_products(self, verbose=True, print_time=False):
        """Returns a dictionary of product: price for every product in every webpage
        """

        products_by_webpage = dict()
        for webpage in self.webpage_to_object:
            if self.get_url(webpage) is not None:
                if verbose:
                    print(f'Scraping {webpage}...')
                if print_time:
                    initial_time = time.time()
                
                webscraper_instance = self.webpage_to_object[webpage](**self.get_url_keywords(webpage))
                products_by_webpage[webpage] = webscraper_instance.get_products()
                
                if print_time:
                    scraping_time = time.time() - initial_time
                    print(f'Finished scraping {webpage} ({scraping_time:.02f}s)')

        return products_by_webpage
    
    # Complete process
    def check_new_products(self):
        """Verifies if there is a new product for every webpage and sends an email when it occurs
        """
        
        init()  # Initiates colorama
        print(f'{Fore.BLUE + Style.BRIGHT}STARTING WEBSCRAPER!{Style.RESET_ALL} Time: {self.get_current_time()}')

        initial_products_prices = self.get_all_products(verbose=False, print_time=False)
        send_email_flag = True
        alerts = 0
        last_alert = ''
        n = 0
        while True:
            try:
                # Scrap webpages
                new_products_prices = self.get_all_products(verbose=True, print_time=False)
                new_products = {webpage: [] for webpage in new_products_prices}
                # Send email when there is a new product or if a product has been restocked
                for webpage in new_products_prices:
                    for product in new_products_prices[webpage]:
                        if product is not None and product != '':
                            is_new_product = product not in initial_products_prices[webpage]
                            was_product_restocked = False
                            if not is_new_product:
                                was_product_restocked = initial_products_prices[webpage][product] == self.NO_STOCK_STATUS and \
                                                        new_products_prices[webpage][product] != self.NO_STOCK_STATUS 
                            if is_new_product or was_product_restocked:
                                webpage_new_products_list = new_products[webpage]
                                webpage_new_products_list.append(product)
                                new_products[webpage] = webpage_new_products_list
                                send_email_flag = True
                
                initial_products_prices = new_products_prices.copy()

                if send_email_flag:
                    self.send_email(products_prices=new_products_prices, new_products=new_products)
                    if n == 0:
                        print(f'{Fore.YELLOW + Style.BRIGHT}FIRST SCRAPING{Style.RESET_ALL} E-mail has been sent. Time: {self.get_current_time()}')
                    else:
                        print(f'{Fore.GREEN}NEW PRODUCTS ALERT!{Style.RESET_ALL} E-mail has been sent. Time: {self.get_current_time()}')
                        for webpage in new_products:
                            for product in new_products[webpage]:
                                print(f'\t{webpage}: {Fore.GREEN}{product}{Style.RESET_ALL} ({new_products_prices[webpage][product]})')
                        alerts += 1
                        last_alert = self.get_current_time()
                    send_email_flag = False
                else:
                    print(f'{Fore.YELLOW + Style.BRIGHT}NOTHING NEW{Style.RESET_ALL}. Time: {self.get_current_time()}. Alerts: {alerts}{f" (last: {last_alert})" if alerts > 0 else ""}')
            except Exception as e:
                print(f"Error: '{e}'. Time: {self.get_current_time()}")
                continue
            
            n += 1
            time.sleep(self.timeout * 60)

    def send_email(self, products_prices, new_products):
        # Start e-mail server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()

        server.login(user=self.username, password=self.password)

        # Setup e-mail message
        message = MIMEMultipart('alternative')
        message['Subject'] = self.email_subject
        message['From'] = 'Webscraping Bot'
        message['To'] = (', ').join(self.to_address) if isinstance(self.to_address, list) else self.to_address
        body = self.setup_email_html(products_prices,new_products)
        body = MIMEText(body.encode('utf-8'), 'html', _charset='utf-8')
        message.attach(body)

        server.sendmail(from_addr=self.username, to_addrs=self.to_address, msg=message.as_string())
        
        server.quit()
    
    def setup_email_html(self, products_prices, new_products):
        HTML_HEAD = """<html>
            <head>
            <style>
                h3 { font-size: 1.3em }
            </style>
            </head>
            <body>"""
        HTML_END = """</body>
            </html>"""
        
        html = HTML_HEAD
        for webpage in products_prices:
            html += self.webpage_html(webpage)
            products_dict = products_prices[webpage]
            if len(products_dict) > 0:
                for product, price in products_dict.items():
                    html += self.product_html(product, price, new_products[webpage])
            html += self.url_html(self.urls_keywords_dict[webpage]['URL'])
            html += '<br>'
        html += HTML_END

        return html

    def webpage_html(self, webpage):
        return f'<h3>{webpage}</h3>'
        
    def product_html(self, product, price, new_products_list):
        price_html = price
        if price == self.NO_STOCK_STATUS:
            price_html = f'<span style="color: red";>{price}</span>'
        new_product_html = '<span style="color: green; font-weight: bold">(NEW) </span>' \
                                if product in new_products_list else ''
        return f'<li>{new_product_html}{product}: {price_html}</li>'
    
    def url_html(self, url):
        return f'<p>URL: <a href="{url}" target="_blank">{url}</a></p>'

# Read and process config.json file
with open('config.json', encoding='utf-8') as f:
    params = json.load(f)
    urls_keywords = params['URLS_KEYWORDS']
    for webpage in urls_keywords:
        keywords = urls_keywords[webpage]['keywords']
        if isinstance(keywords, str) and keywords.lower() == 'none':
            urls_keywords[webpage]['keywords'] = None
    email_subject = params['EMAIL_SUBJECT']
    timeout = params['TIMEOUT']
    chromedriver_path = params['CHROMEDRIVER_PATH']

def main():
    ws = Webscraper(urls_keywords_dict=urls_keywords, email_subject=email_subject, username=username,
                    password=password, to_address=to_address, timeout=timeout)
    ws.check_new_products()

if __name__ == '__main__':
    main()
