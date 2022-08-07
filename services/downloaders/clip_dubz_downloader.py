import requests
from lxml.html import fromstring


class ClipDubzDownloader:

    @staticmethod
    def get_video_content(url):
        response = requests.get(url)
        html = fromstring(response.text)
        return requests.get(html.xpath("//video/source/@src")[0]).content
