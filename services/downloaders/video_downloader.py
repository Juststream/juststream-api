from typing import Final

import requests

from helpers.url_helper import get_website_host
from services.downloaders.clippituser_downloader import ClippituserDownloader
from services.downloaders.foddergg_downloader import FodderggDownloader
from services.downloaders.gfycat_downloader import GfycatDownloader
from services.downloaders.mixturegg_downloader import MixtureggDownloader
from services.downloaders.reddit_downloader import RedditDownloader
from services.downloaders.scuffedentertainment_downloader import ScuffedentertainmentDownloader
from services.downloaders.streamable_downloader import StreamableDownloader
from services.downloaders.streamff_downloader import StreamffDownloader
from services.downloaders.streamgg_downloader import StreamggDownloader
from services.downloaders.streamja_downloader import StreamjaDownloader
from services.downloaders.streamwo_downloader import StreamwoDownloader
from services.downloaders.streamye_downloader import StreamyeDownloader
from services.downloaders.twitter_downloader import TwitterDownloader
from services.downloaders.youtube_downloader import YoutubeDownloader
from services.downloaders.clip_dubz_downloader import ClipDubzDownloader

VIDEO_DOWNLOADER_MAP: Final = {
    'reddit.com': RedditDownloader,
    'v.redd.it': RedditDownloader,
    'redd.it': RedditDownloader,
    'streamable.com': StreamableDownloader,
    'twitter.com': TwitterDownloader,
    'youtube.com': YoutubeDownloader,
    'youtu.be': YoutubeDownloader,
    'streamwo.com': StreamwoDownloader,
    'streamja.com': StreamjaDownloader,
    'clippituser.tv': ClippituserDownloader,
    'streamye.com': StreamyeDownloader,
    'gfycat.com': GfycatDownloader,
    'scuffedentertainment.com': ScuffedentertainmentDownloader,
    'streamff.com': StreamffDownloader,
    'streamgg.com': StreamggDownloader,
    'mixture.gg': MixtureggDownloader,
    'v.fodder.gg': FodderggDownloader,
    'clip.dubz.co': ClipDubzDownloader
}


class VideoDownloader:

    def __init__(self, url):
        self.url = url
        self.website_host = get_website_host(url).replace('www.', '')

    def get_video_content(self):
        if self.url.split('?')[0].endswith('.mp4') or self.url.split('?')[0].endswith('.ts'):
            return requests.get(self.url).content
        video_downloader = VIDEO_DOWNLOADER_MAP.get(self.website_host)
        if video_downloader:
            return video_downloader.get_video_content(self.url)
