
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
