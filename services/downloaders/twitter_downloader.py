import json
import re

import requests


class TwitterDownloader:
    def _get_video_url(self, post_link):
        video_id = (
            post_link.split("/")[5].split("?")[0]
            if "s?=" in post_link
            else post_link.split("/")[5]
        )
        self.log = {}
        sources = {
            "post_link": "https://twitter.com/i/videos/tweet/" + video_id,
            "activation_ep": "https://api.twitter.com/1.1/guest/activate.json",
            "api_ep": "https://api.twitter.com/1.1/statuses/show.json?id=" + video_id,
        }
        headers = {
            "User-agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-language": "es-419,es;q=0.9,es-ES;q=0.8,en;q=0.7,en-GB;q=0.6,en-US;q=0.5",
        }
        self.session = requests.Session()

        def send_request(self, url, method, headers):
            request = (
                self.session.get(url, headers=headers)
                if method == "GET"
                else self.session.post(url, headers=headers)
            )
            if request.status_code == 200:
                return request.text

        # get guest token
        token_request = send_request(self, sources["post_link"], "GET", headers)
        bearer_file = re.findall('src="(.*js)', token_request)
        file_content = send_request(self, str(bearer_file[0]), "GET", headers)
        bearer_token_pattern = re.compile("Bearer ([a-zA-Z0-9%-])+")
        bearer_token = bearer_token_pattern.search(file_content)
        headers["authorization"] = bearer_token.group(0)
        self.log["bearer"] = bearer_token.group(0)
        req2 = send_request(self, sources["activation_ep"], "post", headers)
        headers["x-guest-token"] = json.loads(req2)["guest_token"]
        self.log["guest_token"] = json.loads(req2)["guest_token"]
        # get link
        self.log["full_headers"] = headers
        api_request = send_request(self, sources["api_ep"], "GET", headers)
        videos = json.loads(api_request)["extended_entities"]["media"][0]["video_info"][
            "variants"
        ]
        self.log["vid_list"] = videos
        bitrate = 0
        for vid in videos:
            if vid["content_type"] == "video/mp4":
                if vid["bitrate"] < 1000000:
                    return vid["url"]
        return None

    def get_video_content(self, post_link):
        video_url = self._get_video_url(post_link)
        return requests.get(video_url).content
