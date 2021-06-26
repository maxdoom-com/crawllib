from unidecode import unidecode
import re

def slugify(text):
    """slugifies a string"""
    
    text = unidecode(text).lower()
    slug = re.sub(r'[\W_]+', '-', text)

    while slug.endswith('-'):
        slug = slug[:-1]

    while slug.startswith('-'):
        slug = slug[1:]

    return slug
