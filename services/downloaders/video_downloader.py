import requests

from helpers.url_helper import get_website_host
from services.downloaders.clippituser_downloader import ClippituserDownloader
from services.downloaders.gfycat_downloader import GfycatDownloader
from services.downloaders.reddit_downloader import RedditDownloader
from services.downloaders.scuffedentertainment_downloader import ScuffedentertainmentDownloader
from services.downloaders.streamable_downloader import StreamableDownloader
from services.downloaders.streamff_downloader import StreamffDownloader
from services.downloaders.streamja_downloader import StreamjaDownloader
from services.downloaders.streamwo_downloader import StreamwoDownloader
from services.downloaders.streamye_downloader import StreamyeDownloader
from services.downloaders.twitter_downloader import TwitterDownloader
from services.downloaders.youtube_downloader import YoutubeDownloader


class VideoDownloader:

    def __init__(self, url):
        self.url = url
        self.website_host = get_website_host(url).replace('www.', '')

    def get_video_content(self):
        if self.url.split('?')[0].endswith('.mp4') or self.url.split('?')[0].endswith('.ts'):
            return requests.get(self.url).content
        elif self.website_host == 'reddit.com' or self.website_host == 'redd.it' or self.website_host == 'v.redd.it':
            return RedditDownloader().get_video_content(self.url)
        elif self.website_host == 'streamable.com':
            return StreamableDownloader().get_video_content(self.url)
        elif self.website_host == 'twitter.com':
            return TwitterDownloader().get_video_content(self.url)
        elif self.website_host == 'youtube.com' or self.website_host == 'youtu.be':
            return YoutubeDownloader().get_video_content(self.url)
        elif self.website_host == 'streamwo.com':
            return StreamwoDownloader().get_video_content(self.url)
        elif self.website_host == 'streamja.com':
            return StreamjaDownloader().get_video_content(self.url)
        elif self.website_host == 'clippituser.tv':
            return ClippituserDownloader().get_video_content(self.url)
        elif self.website_host == 'streamye.com':
            return StreamyeDownloader().get_video_content(self.url)
        elif self.website_host == 'gfycat.com':
            return GfycatDownloader().get_video_content(self.url)
        elif self.website_host == 'scuffedentertainment.com':
            return ScuffedentertainmentDownloader().get_video_content(self.url)
        elif self.website_host == 'streamff.com':
            return StreamffDownloader().get_video_content(self.url)
