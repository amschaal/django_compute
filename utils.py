def merge(destination, source):
    for key, value in source.items():
        if isinstance(value, dict):
            # get node or create one
            node = destination.setdefault(key, {})
            merge(node, value)
        else:
            destination[key] = value
    return destination