"""A small collection of functionalities to crawl the web."""

# external dependencies imported as private identifiers, so a
#   from crawllib import *
# does not import these...
import requests as _requests
from io import StringIO as _StringIO
from lxml import etree as _etree
from urllib.parse import urlparse as _urlparse
from unidecode import unidecode as _unidecode
import re as _re
from shutil import copyfileobj as _copyfileobj
from os import makedirs as _makedirs, path as _path


class GetPageError(Exception):
    """
    An error indicating that we were unable to load a page.
    """


def load(url):
    """
    Loads a page from an url.
    """
    
    r = _requests.get(url)
    if not r.status_code == 200:
        raise( GetPageError(f"Error while downloading {url}. Status code: {r.status_code}. Response: {r}.") )

    return _etree.parse(_StringIO(r.text), _etree.HTMLParser()).getroot()


def load_text(text):
    """
    Loads a page from text.
    """
    
    return _etree.parse(_StringIO(text), _etree.HTMLParser()).getroot()


def slugify(text):
    """slugifies a string"""
    
    text = _unidecode(text).lower()
    slug = _re.sub(r'[\W_]+', '-', text)

    while slug.endswith('-'):
        slug = slug[:-1]

    while slug.startswith('-'):
        slug = slug[1:]

    return slug


def preprend_if_missing(domain, url):
    """
    Preprend a protocol://domain/ to an url, if it is missing.
    """
    
    if not url.startswith(domain):
        return domain + url
    else:
        return url


def download( url, filename, overwrite=False, mkdir=True ):
    """
    Aownload an url as filename.
    Will overwrite existing files, if overwrite is true.
    Makes missing dirs if mkdir is true.
    """
    
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


def for_all(tree, selector, callback):
    """
    Iterate over all elements in :tree matching the cssselect :selector
    and call :callback
    """
    
    for element in tree.cssselect(selector):
        callback(element)


def for_one(tree, selector, callback):
    """
    Find the first elements in :tree matching the cssselect :selector
    and call :callback
    """
    
    for element in tree.cssselect(selector):
        callback(element)
        return


class PageLoader:
    """
    Loads a page.
    """

    def __init__(self, url, text=None):
        """
        Load a page from an url and make it available as :content.
        Calculates the :baseurl of the page.
        """

        # setup basics
        self._baseurl  = None
        self.content   = None
        self.url       = url
        self.baseurl   = url

        # load the content
        if text is not None:
            self._load_text(text)

        else:
            self._load_url(url)
        
        # override the baseurl from <base href="...">
        def set_baseurl(base):
            url = base.get("href", None)
            if url is not None and url != "/":
                self.baseurl = url

        for_one(self.content, "base", set_baseurl)


    @property
    def baseurl(self):
        """Returns the baseurl."""
        return self._baseurl

    
    @baseurl.setter
    def baseurl(self, url):
        """
        Parses the url and sets the baseurl.
        Removes get parameters (...?x=y) and fragments (...#foo).
        Removes the document like (.../index.html).
        """

        parsed = _urlparse(url)

        scheme   = parsed.scheme
        hostname = parsed.hostname
        port     = parsed.port
        path     = parsed.path

        ##
        ## calulating the base url
        ##
        self._baseurl = f"{scheme}://{hostname}"
        if port is not None:
            self._baseurl += ":"+port
        if path.endswith('/'):
            self._baseurl += path
        else:
            self._baseurl += '/'.join( path.split('/')[:-1] )


    def _load_url(self, url):
        self.content   = load(url)

    def _load_text(self, text):
        self.content   = load_text(text)

    def make_absolute(self, tag, attribute):
        """
        Patch links or forms or images to refer to absolute urls, if possible.
        """
        
        def patch_url(element):
            url = element.get(attribute, None)

            if url is None:
                pass # do nothing
            
            elif url.startswith(self.baseurl):
                pass # do nothing
            
            elif url.startswith('//'):
                element.set(attribute, self._scheme + url)
            
            elif url.startswith('/'):
                element.set(attribute, self.baseurl + url[1:])
            
            elif _re.match(f'[a-z]+:', url) is not None:
                pass # do nothing
            
            else:
                element.set(attribute, self.baseurl + url)

        for_all(self.content, tag, patch_url)


    def make_absolute_links(self):
        """
        Make links absolute.
        """
        
        self.make_absolute("a", "href")
