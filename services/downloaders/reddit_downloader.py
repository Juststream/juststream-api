import requests

from services.reddit_service import RedditClient


class RedditDownloader:
    def __init__(self):
        self.reddit_service = RedditClient("juststream")

    def get_video_content(self, reddit_link: str):
        post = self.reddit_service.reddit.submission(url=reddit_link)
        return requests.get(post.media["reddit_video"]["fallback_url"]).content
