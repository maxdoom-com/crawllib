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

## Use an objective approach

```py
from crawllib import *

p = PageLoader("https://github.com/maxdoom-com/crawllib")
p.make_absolute_links() # will try to make all links absolute

def print_a(a):
    print(a.get("href"))
for_all(p.content, "a", print_a) # will call print_a() for every <a> found

```

## Iterating with callbacks

I've added to procs to iterate over (cssselect) nodes:

- `for_all(tree, selector, callback)` will call the callback for all nodes found with tree.cssselect(selector)
- `for_one(tree, selector, callback)` will call the callback for the first node found with tree.cssselect(selector)

```py
from crawllib import *

p = PageLoader("https://github.com/maxdoom-com/crawllib")
p.make_absolute_links()
# Will try to make all links absolute to the given url or
# the <base href="..."> in the html code.
# The base-tag overrides the url when calculating the baseurl.

def first_a(a):
    print(a.get("href"))

def each_div(div):
    for_one(div, "a", first_a)

for_all(p.content, "div", each_div) # will call each_div() for each <div> found
```

## Loading a string

You may now load a string as html.

```py
from crawllib import *

html = load_text("""<html>...</html>""")
```

And you may use the PageLoader class as well:

```py
from crawllib import *

p = PageLoader("http://some.fake/do/main", """<html>...</html>""")
p.make_absolute_links()
```



Installation
------------

```sh
pip install git+https://github.com/maxdoom-com/crawllib
```
