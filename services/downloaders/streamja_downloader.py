import requests
from lxml.html import fromstring


class StreamjaDownloader:
    @staticmethod
    def get_video_content(url):
        response = requests.get(url)
        html = fromstring(response.text)
        retries = 10
        while retries:
            try:
                return requests.get(html.xpath("//video/source/@src")[0]).content
            except requests.exceptions.SSLError or requests.exceptions.ConnectionError:
                retries -= 1
