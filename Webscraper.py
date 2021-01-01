import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
from datetime import datetime
from FravegaWebscraper import FravegaWebscraper
from CetrogarWebscraper import CetrogarWebscraper
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
            'Frávega': FravegaWebscraper(url=self.urlsKeywordsDict['Frávega']['URL'],
                                         keywords=self.urlsKeywordsDict['Frávega']['keywords']),
            'Cetrogar': CetrogarWebscraper(url=self.urlsKeywordsDict['Cetrogar']['URL'],
                                           keywords=self.urlsKeywordsDict['Cetrogar']['keywords'])
        }
    
    def __repr__(self):
        return f'{self.__class__.__name__}({self.urlsKeywordsDict})'
    
    def __str__(self):
        return f'{self.__class__.__name__}: {self.urlsKeywordsDict}'
    
    def checkProducts(self):
        return {webpage: self.webpageToObject[webpage].checkProducts() for webpage in self.webpageToObject}
    
        # Complete process
    def checkNewProducts(self):
        initial_products_prices = self.checkProducts()
        send_email_flag = True
        while True:
            now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            
            new_products_prices = self.checkProducts()
            for webpage in new_products_prices:
                for product in new_products_prices[webpage]:
                    # Send email when there is a new product
                    if product != '' and product not in initial_products_prices[webpage]:
                        send_email_flag = True
                        break
            
            if send_email_flag:
                self.sendEmail(productsPrices=new_products_prices)
                print(f'E-mail has been sent. Time: {now}')
                initial_products_prices = new_products_prices
                send_email_flag = False
            else:
                print(f'Nothing new. Time: {now}')
            
            time.sleep(self.timeout * 60)

    # Notification
    def sendEmail(self, productsPrices):
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
            body += f'{webpage.upper()}:\n'
            for product, price in productsPrices[webpage].items():
                body += f'- {product}: {price}\n'
            body += f"\nURL: {self.urlsKeywordsDict[webpage]['URL']}\n\n\n"
        body = MIMEText(body.encode('utf-8'), 'plain', _charset='utf-8')
        message.attach(body)

        server.sendmail(from_addr=self.username, to_addrs=self.toAddress, msg=message.as_string())
        
        server.quit()


# Start
ws = Webscraper(urlsKeywordsDict=URLS_KEYWORDS, emailSubject=EMAIL_SUBJECT, username=USERNAME,
                password=PASSWORD, toAddress=TO_ADDRESS, timeout=TIMEOUT)
ws.checkNewProducts()
