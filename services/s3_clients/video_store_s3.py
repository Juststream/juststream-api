from time import time

import boto3

from services.s3_clients.base_s3_client import S3Client


class VideoStoreS3(S3Client):

    def __init__(self):
        super().__init__('m3u8-files-mate')
        self.cloudfront = boto3.client('cloudfront')

    def invalidate_cache(self, video_id):
        self.cloudfront.create_invalidation(
            DistributionId='E2VO5R1C606TBW',
            InvalidationBatch={
                'Paths': {
                    'Quantity': 1,
                    'Items': [
                        f'/{video_id}/*'
                    ],
                },
                'CallerReference': str(time()).replace(".", "")
            }
        )

    def remove_video(self, video_id):
        old_path = video_id + '/video.m3u8'
        new_path = video_id + '/video-removed.m3u8'
        copy_source = {'Bucket': self.bucket, 'Key': old_path}
        self._s3.copy_object(CopySource=copy_source, Bucket=self.bucket, Key=new_path)
        self._s3.delete_object(Bucket=self.bucket, Key=old_path)
        self.invalidate_cache(video_id)


if __name__ == '__main__':
    VideoStoreS3().remove_video('PioneeringLaypersonCaving')
