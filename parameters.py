from secrets import username, password, to_address

# Si no querés usar keywords, reemplazar todo el corchete por None. Ejemplo:
#   'keywords': None
URLS_KEYWORDS = {
        'Frávega': {
            'URL': 'https://www.fravega.com/l/?keyword=3080',
            'keywords': ['PS5', 'Playstation 5', 'Play station 5']},
        'Cetrogar': {
            'URL': 'https://www.cetrogar.com.ar/catalogsearch/result/?q=ps5',
            'keywords': ['PS5', 'Playstation 5', 'Play station 5']},
    }
EMAIL_SUBJECT = 'Hay nuevos productos de PS5'
USERNAME = username
PASSWORD = password
TO_ADDRESS = to_address
TIMEOUT = 1  # Minutes