import requests
from io import StringIO
from lxml import etree

class GetPageError(Exception):
    """
    An error indicating that we were unable to load a page.
    """

def load(url):
    """
    Loads a page from an url.
    """
    
    r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',})
    if not r.status_code == 200:
        raise( GetPageError(f"Error while downloading {url}. Status code: {r.status_code}. Response: {r}.") )

    return etree.parse(StringIO(r.text), etree.HTMLParser()).getroot()


def load_text(text):
    """
    Loads a page from text.
    """
    
    return etree.parse(StringIO(text), etree.HTMLParser()).getroot()
