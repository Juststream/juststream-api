import requests


class ClippituserDownloader:

    @staticmethod
    def get_video_content(url: str):
        video_id = url.split('/c/')[1].split('?')[0].split('/')[0]
        return requests.get(f'https://clips.clippit.tv/{video_id}/360.mp4').content
