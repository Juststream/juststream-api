import requests
from lxml.html import fromstring


class GfycatDownloader:
    @staticmethod
    def get_video_content(url: str):
        response = requests.get(url)
        html = fromstring(response.text)
        return requests.get(html.xpath("//video/source/@src")[1]).content
