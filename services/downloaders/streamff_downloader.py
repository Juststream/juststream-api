import requests


class StreamffDownloader:

    @staticmethod
    def get_video_content(url):
        video_id = url.split('/v/')[-1].split('?')[0].rstrip('/')
        response = requests.get(f'https://streamff.com/api/videos/{video_id}')
        body = response.json()
        if not body['uploaded']:
            return
        return requests.get(f'https://streamff.com{body["videoLink"]}').content
