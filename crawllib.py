"""A small collection of functionalities to crawl the web."""

class GetPageError(Exception):
    """An error indicating that we were unable to load a page"""

def load(url):
    """Loads a page from a url."""

    import requests, io
    from lxml import etree
    
    r = requests.get(url)
    if not r.status_code == 200:
        raise( GetPageError(f"Error while downloading {url}. Status code: {r.status_code}. Response: {r}.") )

    return etree.parse(io.StringIO(r.text), etree.HTMLParser()).getroot()


def slugify(text):
    """slugifies a string"""
    import unidecode, re
    
    text = unidecode.unidecode(text).lower()
    slug = re.sub(r'[\W_]+', '-', text)

    while slug.endswith('-'):
        slug = slug[:-1]

    while slug.startswith('-'):
        slug = slug[1:]

    return slug


def preprend_if_missing(domain, url):
    """preprend a protocol://domain/ to a url, if it is missing"""
    if not url.startswith(domain):
        return domain + url
    else:
        return url


def download( url, target ):
    import requests, shutil

    response = requests.get(url, stream=True)
    with open(target, 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    

