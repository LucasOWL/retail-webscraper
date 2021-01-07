import os
from secrets import username, password, to_address

# Si no querés usar keywords, reemplazar todo el corchete por None. Ejemplo:
#   'keywords': None
keywords = ['PS5', 'Playstation 5', 'Play station 5', 'Dualsense', 'Dual sense', 'Pulse', 'Pulse3D', 'Pulse 3D']
URLS_KEYWORDS = {
        'Frávega': {
            'URL': 'https://www.fravega.com/l/?keyword=ps5',
            'keywords': keywords},
        'Cetrogar': {
            'URL': 'https://www.cetrogar.com.ar/catalogsearch/result/?q=ps5',
            'keywords': keywords},
        'Sony': {
            'URL': 'https://store.sony.com.ar/ps5',
            'keywords': None},
        'Jumbo': {
            'URL': 'https://www.jumbo.com.ar/busca/?ft=ps5',
            'keywords': None},
        'Disco': {
            'URL': 'https://www.disco.com.ar/Comprar/Home.aspx#_atCategory=false&_atGrilla=true&_query=ps5',
            'keywords': None},
        'Vea Digital': {
            'URL': 'https://www.veadigital.com.ar/Comprar/Home.aspx#_atCategory=false&_atGrilla=true&_query=ps5',
            'keywords': None},
        'Falabella': {
            'URL': 'https://www.falabella.com.ar/falabella-ar/category/cat10166/Mundo-gamer?facetSelected=true&f.product.brandName=sony&isPLP=1',
            'keywords': keywords},
        'Walmart': {
            'URL': 'https://www.walmart.com.ar/buscar?text=ps5',
            'keywords': keywords},
    }
EMAIL_SUBJECT = 'Hay nuevos productos de PS5'
USERNAME = username
PASSWORD = password
TO_ADDRESS = to_address
TIMEOUT = 5  # Minutes
CHROMEDRIVER_PATH = os.path.join(r'C:\webdrivers\chromedriver.exe')