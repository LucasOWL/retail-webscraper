from urllib.request import urlopen
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
from datetime import datetime
from secrets import username, password, to_address

# Scraper
def check_products(url, keywords):
    uClient = urlopen(url)
    page_html = uClient.read()
    page_soup = BeautifulSoup(page_html, 'html.parser')
    
    # Find products and prices
    itemsGrid = page_soup.find('ul', {'name': 'itemsGrid'})
    products_li = itemsGrid.find_all('li')
    products_prices = {
        product.h4.text: product.find('div', {'data-test-id': 'product-price'}).span.text
            for product in products_li if any(kw.lower() in product.h4.text.lower() for kw in keywords)}

    uClient.close()

    return products_prices

# Notification
def send_email(productsPrices, url, email_subject, username, password, to_address):
    # Start e-mail server
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login(user=username, password=password)

    # Setup e-mail message
    message = MIMEMultipart('alternative')
    message['Subject'] = email_subject
    message['From'] = 'Webscraping Bot'
    message['To'] = to_address
    body = 'Productos:\n\n'
    for product, price in productsPrices.items():
        body += f'- {product}: {price}\n'
    body += f'\nURL: {url}'
    body = MIMEText(body.encode('utf-8'), 'plain', _charset='utf-8')
    message.attach(body)

    server.sendmail(from_addr=username, to_addrs=to_address, msg=message.as_string())
    
    server.quit()

# Complete process
def check_new_products(url, keywords, email_subject, username, password, to_address, timeout):
    initial_products_prices = check_products(url=url, keywords=keywords)
    send_email_flag = True
    while True:
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        
        new_products_prices = check_products(url=url, keywords=keywords)
        for product in new_products_prices:
            # Send email when there is a new product
            if product not in initial_products_prices:
                send_email_flag = True
                break
        
        if send_email_flag:
            send_email(productsPrices=new_products_prices, url=url, email_subject=email_subject,
                       username=username, password=password, to_address=to_address)
            print(f'E-mail has been sent. Time: {now}')
            initial_products_prices = new_products_prices
            send_email_flag = False
        else:
            print(f'Nothing new. Time: {now}')
        
        time.sleep(timeout * 60)


# ---------------------------------- Parameters ---------------------------------- #
URL = 'https://www.fravega.com/l/?keyword=playstation%205'
KEYWORDS = ['Playstation 5', 'PS5', 'Play Station 5']
EMAIL_SUBJECT = 'Frávega: Hay nuevos productos de PS5'
USERNAME = username
PASSWORD = password
TO_ADDRESS = to_address
TIMEOUT = 1  # Minutes
# -------------------------------------------------------------------------------- #

check_new_products(
    url=URL,
    keywords=KEYWORDS,
    email_subject=EMAIL_SUBJECT,
    username=USERNAME,
    password=PASSWORD,
    to_address=TO_ADDRESS,
    timeout=TIMEOUT)
