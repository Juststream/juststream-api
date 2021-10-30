from urllib.parse import urlparse


def get_website_host(url: str):
    return urlparse(url).netloc
