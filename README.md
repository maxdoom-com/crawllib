crawllib
========================================================================

A small collection of functionalities to crawl the web.


Requirements
------------------------------------------------------------------------

These python libraries are required:

- requests
- unidecode
- lxml
- cssselect
- urllib

Example 1
------------------------------------------------------------------------

... getting all links

```py
from crawllib import *

(html, headers, status_code) = load("http://example.org/")
for a in html.cssselect("a"):
    print( a.get("href") )
```


Example 2
------------------------------------------------------------------------

... downloading images

```py
from crawllib import *

content_type = download(
    "https://www.iana.org/_img/2013.1/iana-logo-header.svg",
    slugify("i a n a")+".svg"
)
download(
    "https://www.iana.org/_img/2013.1/iana-logo-header.svg",
    "/_img/2013.1/iana-logo-header.svg",
    overwrite=True,
    mkdir=True
)
```


Use an objective approach
------------------------------------------------------------------------


```py
from crawllib import *

p = PageLoader("https://github.com/maxdoom-com/crawllib")
p.make_absolute_links() # will try to make all links absolute

def print_a(a):
    print(a.get("href"))
for_all(p.content, "a", print_a) # will call print_a() for every <a> found

```


Iterating with callbacks
------------------------------------------------------------------------

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

Loading a string
------------------------------------------------------------------------

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


Storing text in a database
------------------------------------------------------------------------

I've added a simple sqlite3 database class.

```py
from crawllib import Database

db = Database("my.db")

db.executescript("""
    CREATE TABLE IF NOT EXISTS pages ( id INTEGER PRIMARY KEY, url NOT NULL, text);
""")

db.execute("INSERT INTO pages ( url, text ) VALUES(:url, :text)",{
    'url': "http://some.fake/do/main",
    'text': """<html>...</html>"
})

for page in db.select("SELECT * FROM pages"):
    print(page)
```


Converting a node back to text
------------------------------------------------------------------------

```py
from crawllib import *

p = PageLoader("http://some.fake/do/main", """<html>...</html>""")
print(p.tostring())

def print_a_text(a):
    print(element2text(a))

for_all(p.content, "a", print_a_text)
```


A simple key-value storage
------------------------------------------------------------------------

Create a store:

```py
db.create("Tests", "foo", "bar", "blub")
```
---

Drop a store:

```py
db.drop("Tests")
```

---

Store key/value pairs:

```py
db.store("Tests", "test-1-2-3", {"foo":1, "bar":2, "blub":3})
db.store("Tests", "test-1-2-3", {"foo":3, "bar":2, "blub":1})
db.store("Tests", "test-1-2-3 A", {"foo":1, "bar":2, "blub":3})

---

Remove an entry:

```py
db.remove("Tests", "test-1-2-3 A")
```

---

Print a record:

```py
print(db.get("Tests", "test-1-2-3"))
```

---

Get all entries:

```py
for entry in db.all(self, store):
    print(entry)
```

---

Clear a store:

```py
db.empty("Tests")
```


Installation
------------------------------------------------------------------------

```sh
pip install git+https://github.com/maxdoom-com/crawllib
```
