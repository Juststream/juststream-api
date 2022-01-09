from helpers.datetime_helper import get_current_timestamp
from services.dynamodb_clients.reports_table import ReportsTable
from services.dynamodb_clients.videos_table import VideosTable
from services.media_convert_service import MediaConvertClient
from services.random_name_service import get_random_name
from services.s3_clients.video_store_s3 import VideoStoreS3

video_store_s3 = VideoStoreS3()
media_convert_client = MediaConvertClient()
videos_table = VideosTable()
reports_table = ReportsTable()


class VideosController:

    @staticmethod
    def create_video_from_s3_paths(s3_paths: list, video_id: str) -> dict:
        job_id = media_convert_client.create_streaming_videos(s3_paths, video_id)
        item = videos_table.put_item(
            {
                'id': video_id,
                'media_convert_job_id': job_id,
                'views': 1,
                'created_at': get_current_timestamp(),
                'status': 'SUBMITTED'
            }
        )
        return item

    def upload_video(self, file_object: bytes) -> dict:
        video_id = get_random_name()
        s3_path = f'{video_id}/video.mp4'
        video_store_s3.upload_file(file_object, s3_path)
        return self.create_video_from_s3_paths([f's3://m3u8-files-mate/{s3_path}'], video_id)

    def upload_video_from_path(self, file_path: str) -> dict:
        video_id = get_random_name()
        s3_path = f'{video_id}/video.mp4'
        video_store_s3.upload_from_path(file_path, s3_path)
        return self.create_video_from_s3_paths([f's3://m3u8-files-mate/{s3_path}'], video_id)

    def upload_multiple_videos_as_one(self, file_objects: list) -> dict:
        video_id = get_random_name()
        file_paths = []
        for index, file_object in enumerate(file_objects):
            if index == 0:
                filepath = f'{video_id}/video.webm'  # hacky
            else:
                filepath = f'{video_id}/video{str(index)}.webm'
            video_store_s3.upload_file(file_object, filepath)
            file_paths.append(f's3://m3u8-files-mate/{filepath}')
        return self.create_video_from_s3_paths(file_paths, video_id)

    @staticmethod
    def get_top_videos() -> list:
        top_videos = []
        for video in videos_table.get_all_time_top():
            top_videos.append({
                'id': video['id'],
                'thumbnail': f'https://d2udncs3qw19a6.cloudfront.net/{video["id"]}/videoposter.0000001.jpg',
                'views': video['views']
            })
        return top_videos

    @staticmethod
    def get_video(video_id: str) -> dict:
        return videos_table.get_item(video_id)

    @staticmethod
    def increment_views(video_id: str) -> dict:
        return videos_table.increment_views(video_id)

    @staticmethod
    def report_video(video_id: str) -> None:
        reports_table.put_item(
            {
                'id': video_id,
                'created_at': get_current_timestamp(),
            }
        )

    @staticmethod
    def get_related_videos(video_id) -> list:
        video = videos_table.get_item(video_id)
        match_id = video.get('match_id')
        if not match_id:
            return []
        related_videos = []
        for video in videos_table.get_items_by_match_id(match_id, video['created_at']):
            related_videos.append(
                {
                    'id': video['id'],
                    'views': video['views'],
                    'title': video.get('video_title')
                }
            )
        return related_videos
