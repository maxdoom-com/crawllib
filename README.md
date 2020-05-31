# crawllib

A small collection of functionalities to crawl the web.


## Requirements

These python libraries are required:

- requests
- unidecode
- lxml


## Example

... getting all links

```py
from crawllib import *

html = load("http://example.org/")
for a in html.cssselect("a"):
    print( preprend_if_missing("http://example.org/", a.get("href")) )
```

## Example 2

... downloading images

```py
from crawllib import *

content_type = download( "https://www.iana.org/_img/2013.1/iana-logo-header.svg", slugify("i a n a")+".svg" )
download( "https://www.iana.org/_img/2013.1/iana-logo-header.svg", "/_img/2013.1/iana-logo-header.svg", overwrite=True, mkdir=True )
```


Installation
------------

```sh
pip install git+https://github.com/maxdoom-com/crawllib
```
