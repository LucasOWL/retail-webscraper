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
        self.NO_STOCK_STATUS = BaseWebscraper.NO_STOCK_STATUS
    
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
    
    def getCurrentTime(self):
        return datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
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
        print(f'{Fore.BLUE}STARTING WEBSCRAPER!{Style.RESET_ALL} Time: {self.getCurrentTime()}')

        initial_products_prices = self.getAllProducts(verbose=False)
        send_email_flag = True
        alerts = 0
        last_alert = ''
        n = 0
        while True:
            now = self.getCurrentTime()
            try:
                # Scrap webpages
                new_products_prices = self.getAllProducts(verbose=True)
                new_products = {webpage: [] for webpage in new_products_prices}
                # Send email when there is a new product or if a product has been restocked
                for webpage in new_products_prices:
                    for product in new_products_prices[webpage]:
                        if product is not None and product != '':
                            is_new_product = product not in initial_products_prices[webpage]
                            product_restocked_flag = False
                            if not is_new_product:
                                product_restocked_flag = initial_products_prices[webpage][product] == self.NO_STOCK_STATUS and \
                                                         new_products_prices[webpage][product] != self.NO_STOCK_STATUS 
                            if is_new_product or product_restocked_flag:
                                webpage_new_products_list = new_products[webpage]
                                webpage_new_products_list.append(product)
                                new_products[webpage] = webpage_new_products_list
                                send_email_flag = True

                if send_email_flag:
                    self.sendEmail(productsPrices=new_products_prices, newProducts=new_products)
                    if n == 0:
                        print(f'{Fore.YELLOW}FIRST SCRAPING{Style.RESET_ALL} E-mail has been sent. Time: {now}')
                    else:
                        print(f'{Fore.GREEN}NEW PRODUCTS ALERT!{Style.RESET_ALL} E-mail has been sent. Time: {now}')
                        alerts += 1
                        last_alert = self.getCurrentTime()
                    send_email_flag = False
                    initial_products_prices = new_products_prices
                else:
                    print(f'{Fore.YELLOW}NOTHING NEW{Style.RESET_ALL}. Time: {now}. Alerts: {alerts}{f" (last: {last_alert})" if alerts > 0 else ""}')
            except Exception as e:
                print(f"Error: '{e}'. Time: {now}")
                continue
            
            n += 1
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
        message['To'] = (', ').join(self.toAddress) if isinstance(self.toAddress, list) else self.toAddress
        body = self.setupEmailHTML(productsPrices, newProducts)
        body = MIMEText(body.encode('utf-8'), 'html', _charset='utf-8')
        message.attach(body)

        server.sendmail(from_addr=self.username, to_addrs=self.toAddress, msg=message.as_string())
        
        server.quit()
    
    def setupEmailHTML(self, productsPrices, newProducts):
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
        for webpage in productsPrices:
            html += self.webpageHTML(webpage)
            products_dict = productsPrices[webpage]
            if len(products_dict) > 0:
                for product in products_dict:
                    price = products_dict[product]
                    html += self.productHTML(product, price, newProducts[webpage])
            html += self.urlHTML(self.urlsKeywordsDict[webpage]['URL'])
            html += '<br>'
        html += HTML_END

        return html

    def webpageHTML(self, webpage):
        return f'<h3>{webpage}</h3>'
        
    def productHTML(self, product, price, newProductsList):
        price_html = price
        if price == self.NO_STOCK_STATUS:
            price_html = f'<span style="color: red";>{price}</span>'
        new_product_html = '<span style="color: green; font-weight: bold">(NUEVO) </span>' \
                                if product in newProductsList else ''
        return f'<li>{new_product_html}{product}: {price_html}</li>'
    
    def urlHTML(self, url):
        return f'<p>URL: <a href="{url}" target="_blank">{url}</a></p>'


# Start
ws = Webscraper(urlsKeywordsDict=URLS_KEYWORDS, emailSubject=EMAIL_SUBJECT, username=USERNAME,
                password=PASSWORD, toAddress=TO_ADDRESS, timeout=TIMEOUT)
ws.checkNewProducts()
