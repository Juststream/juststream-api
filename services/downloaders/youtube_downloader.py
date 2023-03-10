import io

from pytube import YouTube


class YoutubeDownloader:
    @staticmethod
    def get_video_content(youtube_url):
        youtube = YouTube(youtube_url)
        try:
            stream = youtube.streams[1]
        except Exception:
            stream = youtube.streams[0]
        bytes_io = io.BytesIO()
        stream.stream_to_buffer(bytes_io)
        bytes_io.seek(0)

        return bytes_io.read()
