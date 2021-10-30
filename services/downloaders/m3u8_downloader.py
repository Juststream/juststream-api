import m3u8
import requests


class M3u8Downloader:

    @staticmethod
    def parse_m3u8(video_host: str, m3u8_url: str):
        session = requests.Session()
        m3u8_response = session.get(m3u8_url)
        playlist = m3u8.loads(m3u8_response.text)
        playlist = playlist.playlists[-1]
        playlist_url = video_host + playlist.uri
        ts_m3u8_response = session.get(playlist_url)
        ts_m3u8_parse = m3u8.loads(ts_m3u8_response.text)
        chunks = []
        for ts_uri in ts_m3u8_parse.segments.uri:
            ts_file = requests.get(video_host + ts_uri)
            chunks.append(ts_file.content)
        return b''.join(chunks)
