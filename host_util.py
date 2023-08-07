import urllib.parse

# https://stackoverflow.com/a/53172593
def parse_hostport(hp):
    # urlparse() and urlsplit() insists on absolute URLs starting with "//"
    result = urllib.parse.urlsplit('//' + hp)
    return result.hostname, result.port