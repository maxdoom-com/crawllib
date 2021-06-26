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
    
    r = requests.get(url)
    if not r.status_code == 200:
        raise( GetPageError(f"Error while downloading {url}. Status code: {r.status_code}. Response: {r}.") )

    return etree.parse(StringIO(r.text), etree.HTMLParser()).getroot()


def load_text(text):
    """
    Loads a page from text.
    """
    
    return etree.parse(StringIO(text), etree.HTMLParser()).getroot()
