"""A small collection of functionalities to crawl the web."""

from .loaders import load, load_text, GetPageError
from .slugs import slugify
from .downloads import download
from .pageloader import PageLoader
from .iterators import for_one, for_all
from .text import element2text
