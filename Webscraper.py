import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
from datetime import datetime
from colorama import init, Fore, Style
from classes.BaseWebscraper import BaseWebscraper
from classes.FravegaWebscraper import FravegaWebscraper
from classes.CetrogarWebscraper import CetrogarWebscraper
from classes.SonyWebscraper import SonyWebscraper
from classes.JumboWebscraper import JumboWebscraper
from classes.DiscoVeaWebscraper import DiscoVeaWebscraper
from classes.FalabellaWebscraper import FalabellaWebscraper
from classes.WalmartWebscraper import WalmartWebscraper
from classes.GarbarinoWebscraper import GarbarinoWebscraper
from classes.MusimundoWebscraper import MusimundoWebscraper
from parameters import URLS_KEYWORDS, EMAIL_SUBJECT, USERNAME, PASSWORD, TO_ADDRESS, TIMEOUT

class Webscraper(object):

    def __init__(self, urlsKeywordsDict, emailSubject, username, password, toAddress, timeout):
        self.urlsKeywordsDict = urlsKeywordsDict
        self.emailSubject = emailSubject
        self.username = username
        self.password = password
        self.toAddress = toAddress
        self.timeout = timeout
    
        self.webpageToObject = {
            'Frávega': FravegaWebscraper(**self.getURLKeywords('Frávega')),
            'Cetrogar': CetrogarWebscraper(**self.getURLKeywords('Cetrogar')),
            'Sony': SonyWebscraper(**self.getURLKeywords('Sony')),
            'Jumbo': JumboWebscraper(**self.getURLKeywords('Jumbo')),
            'Disco': DiscoVeaWebscraper(**self.getURLKeywords('Disco')),
            'Vea Digital': DiscoVeaWebscraper(**self.getURLKeywords('Vea Digital')),
            'Falabella': FalabellaWebscraper(**self.getURLKeywords('Falabella')),
            'Walmart': WalmartWebscraper(**self.getURLKeywords('Walmart')),
            'Garbarino': GarbarinoWebscraper(**self.getURLKeywords('Garbarino')),
            'Musimundo': MusimundoWebscraper(**self.getURLKeywords('Musimundo')),
        }
    
    def __repr__(self):
        return f'{self.__class__.__name__}({self.urlsKeywordsDict})'
    
    def __str__(self):
        return f'{self.__class__.__name__}: {self.urlsKeywordsDict}'
    
    def getURL(self, webpage):
        """Returns URL from parameters file
        """

        try:
            return self.urlsKeywordsDict[webpage]['URL']
        except:
            return None
    
    def getKeywords(self, webpage):
        """Returns keywords from parameters file
        """
        
        try:
            return self.urlsKeywordsDict[webpage]['keywords']
        except:
            return None
    
    def getURLKeywords(self, webpage):
        """Returns dictionary with url, keywords and name for webpage constructor
        """

        return {'url': self.getURL(webpage), 'keywords': self.getKeywords(webpage), 'name': webpage}
    
    def getAllProducts(self, verbose=True):
        """Returns a dictionary of product: price for every product in every webpage
        """

        products_by_webpage = {}
        for webpage in self.webpageToObject:
            if self.getURL(webpage) is not None:
                if verbose:
                    print(f'Scraping {webpage}...')
                products_by_webpage[webpage] = self.webpageToObject[webpage].getProducts()

        return products_by_webpage
    
    # Complete process
    def checkNewProducts(self):
        """Verifies if there is a new product for every webpage and sends an email when it occurs
        """
        
        init()  # Initiates colorama

        initial_products_prices = self.getAllProducts(verbose=False)
        send_email_flag = True
        while True:
            now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            no_stock_status = BaseWebscraper.NO_STOCK_STATUS

            try:
                # Scrap webpages
                new_products_prices = self.getAllProducts(verbose=True)
                new_products = {webpage: [] for webpage in new_products_prices}
                for webpage in new_products_prices:
                    for product in new_products_prices[webpage]:
                        if product is not None and product != '':
                            is_new_product = product not in initial_products_prices[webpage]
                            product_restocked_flag = False
                            if not is_new_product:
                                product_restocked_flag = initial_products_prices[webpage][product] == no_stock_status and \
                                                         new_products_prices[webpage][product] != no_stock_status 
                            # Send email when there is a new product or if a product has been restocked
                            if is_new_product or product_restocked_flag:
                                webpage_new_products_list = new_products[webpage]
                                webpage_new_products_list.append(product)
                                new_products[webpage] = webpage_new_products_list
                                send_email_flag = True

                if send_email_flag:
                    self.sendEmail(productsPrices=new_products_prices, newProducts=new_products)
                    print(f'{Fore.GREEN}NEW PRODUCTS ALERT!{Style.RESET_ALL} E-mail has been sent. Time: {now}')
                    send_email_flag = False
                    initial_products_prices = new_products_prices
                else:
                    print(f'{Fore.YELLOW}NOTHING NEW{Style.RESET_ALL}. Time: {now}')
            except Exception as e:
                print(f"Error: '{e}'. Time: {now}")
                continue
            
            time.sleep(self.timeout * 60)

    def sendEmail(self, productsPrices, newProducts):
        # Start e-mail server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()

        server.login(user=self.username, password=self.password)

        # Setup e-mail message
        message = MIMEMultipart('alternative')
        message['Subject'] = self.emailSubject
        message['From'] = 'Webscraping Bot'
        message['To'] = self.toAddress
        body = ''
        for webpage in productsPrices:
            new_products = newProducts[webpage]
            body += f'{webpage.upper()}:\n'
            for product in sorted(productsPrices[webpage]):
                new = '(NUEVO) ' if product in new_products else ''
                price = productsPrices[webpage][product]
                body += f'- {new}{product}: {price}\n'
            body += f"\nURL: {self.urlsKeywordsDict[webpage]['URL']}\n\n\n"
        body = MIMEText(body.encode('utf-8'), 'plain', _charset='utf-8')
        message.attach(body)

        server.sendmail(from_addr=self.username, to_addrs=self.toAddress, msg=message.as_string())
        
        server.quit()


# Start
ws = Webscraper(urlsKeywordsDict=URLS_KEYWORDS, emailSubject=EMAIL_SUBJECT, username=USERNAME,
                password=PASSWORD, toAddress=TO_ADDRESS, timeout=TIMEOUT)
ws.checkNewProducts()
