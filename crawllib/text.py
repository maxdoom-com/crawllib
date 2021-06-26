from lxml import etree

def element2text(node, encoding="utf-8"):
    return etree.tostring(node).decode(encoding)
