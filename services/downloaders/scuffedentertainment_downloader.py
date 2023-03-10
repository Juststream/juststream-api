import requests
from lxml.html import fromstring


class ScuffedentertainmentDownloader:
    @staticmethod
    def get_video_content(url: str):
        response = requests.get(url)
        html = fromstring(response.text)
        return requests.get(
            f'https:{html.xpath("//video/source/@src")[0].replace("https:", "")}'
        ).content
