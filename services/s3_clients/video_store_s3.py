from services.s3_clients.base_s3_client import S3Client


class VideoStoreS3(S3Client):

    def __init__(self):
        super().__init__('m3u8-files-mate')
