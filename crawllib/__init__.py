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


def download( url, filename, overwrite=False, mkdir=True ):
    """download an url as filename.
    will overwrite existing files, if overwrite is true.
    makes missing dirs if mkdir is true."""
    
    import requests, shutil, os

    if filename.startswith('/'):
        filename = filename[1:]

    if filename.find('/') != -1 and mkdir:
        dir = '/'.join(filename.split('/')[0:-1])
        os.makedirs(dir, exist_ok=True)

    content_type = None
    
    if not os.path.exists(filename) or overwrite:
        response = requests.get(url, stream=True)
        with open(filename, 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        content_type = headers['content-type']
        del response
    
    return content_type
