from urllib.parse import urlparse
import re
from .loaders import load, load_text
from .iterators import for_one, for_all


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

        parsed   = urlparse(url)

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
            
            elif re.match(f'[a-z]+:', url) is not None:
                pass # do nothing
            
            else:
                element.set(attribute, self.baseurl + url)

        for_all(self.content, tag, patch_url)


    def make_absolute_links(self):
        """
        Make links absolute.
        """
        
        self.make_absolute("a", "href")
