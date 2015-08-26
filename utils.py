
def merge(destination, source):
    for key, value in source.items():
        if isinstance(value, dict):
            # get node or create one
            node = destination.setdefault(key, {})
            merge(node, value)
        else:
            destination[key] = value
    return destination

def sizeof_fmt(num):
#     num /= 1024.0 #function takes bytes, convert to KB 
    for x in ['Bytes','KB','MB','GB']:
        if num < 1024.0 and num > -1024.0:
            return "%3.1f%s" % (num, x)
        num /= 1024.0
    return "%3.1f%s" % (num, 'TB')