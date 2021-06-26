from shutil import copyfileobj
from os import makedirs, path
import requests


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
        makedirs(dir, exist_ok=True)

    content_type = None
    
    if not path.exists(filename) or overwrite:
        response = requests.get(url, stream=True)
        with open(filename, 'wb') as out_file:
            copyfileobj(response.raw, out_file)
        content_type = response.headers.get('content-type', None)
        del response
    
    return content_type
