"""A small collection of functionalities to crawl the web."""

# external dependencies imported as private identifiers, so a
#   from crawllib import *
# does not import these...
import requests as _requests
from io import StringIO as _StringIO
from lxml import etree as _etree
from urllib.parse import urlparse as _urlparse
from unidecode import unidecode as _unidecode
from re import sub as _re_sub
from shutil import copyfileobj as _copyfileobj
from os import makedirs as _makedirs, path as _path


class GetPageError(Exception):
    """An error indicating that we were unable to load a page"""


def load(url):
    """Loads a page from a url."""
    
    r = _requests.get(url)
    if not r.status_code == 200:
        raise( GetPageError(f"Error while downloading {url}. Status code: {r.status_code}. Response: {r}.") )

    return _etree.parse(_StringIO(r.text), _etree.HTMLParser()).getroot()


def slugify(text):
    """slugifies a string"""
    
    text = _unidecode(text).lower()
    slug = _re_sub(r'[\W_]+', '-', text)

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
    
    if filename.startswith('/'):
        filename = filename[1:]

    if filename.find('/') != -1 and mkdir:
        dir = '/'.join(filename.split('/')[0:-1])
        _makedirs(dir, exist_ok=True)

    content_type = None
    
    if not _path.exists(filename) or overwrite:
        response = _requests.get(url, stream=True)
        with open(filename, 'wb') as out_file:
            _copyfileobj(response.raw, out_file)
        content_type = response.headers.get('content-type', None)
        del response
    
    return content_type
