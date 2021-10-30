import requests
from lxml.html import fromstring


class StreamableDownloader:

    @staticmethod
    def get_video_content(url):
        response = requests.get(url)
        html = fromstring(response.text)
        return requests.get(f'https:{html.xpath("//video")[0].attrib["src"]}').content
