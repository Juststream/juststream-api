import boto3


class MediaConvertClient:

    def __init__(self):
        self.media_convert_client = boto3.client(
            'mediaconvert',
            endpoint_url='https://lxlxpswfb.mediaconvert.us-east-1.amazonaws.com',
            region_name='us-east-1'
        )

    def create_streaming_videos(self, input_s3_urls: list, output_id: str):
        output_template = {
            "Settings": {
                "Inputs": [
                    {
                        "TimecodeSource": "ZEROBASED",
                        "VideoSelector": {
                            "Rotate": "AUTO"
                        },
                        "AudioSelectors": {
                            "Audio Selector 1": {
                                "DefaultSelection": "DEFAULT"
                            }
                        },
                        "FileInput": input_s3_url
                    } for input_s3_url in input_s3_urls
                ],
                "OutputGroups": [
                    {
                        "Name": "Apple HLS",
                        "OutputGroupSettings": {
                            "Type": "HLS_GROUP_SETTINGS",
                            "HlsGroupSettings": {
                                "SegmentLength": 10,
                                "MinSegmentLength": 0,
                                "Destination": f"s3://m3u8-files-mate/{output_id}/"
                            }
                        },
                        "Outputs": [
                            {
                                "NameModifier": "360",
                                "Preset": "System-Avc_16x9_360p_29_97fps_1200kbps"
                            },
                            # {
                            #     "Preset": "System-Avc_16x9_720p_29_97fps_6500kbps",
                            #     "NameModifier": "720"
                            # },
                            # {
                            #     "NameModifier": "1080",
                            #     "Preset": "System-Avc_16x9_1080p_29_97fps_8500kbps"
                            # }
                        ],
                        "CustomName": "HLS"
                    },
                    {
                        "Name": "File Group",
                        "OutputGroupSettings": {
                            "Type": "FILE_GROUP_SETTINGS",
                            "FileGroupSettings": {
                                "Destination": f"s3://m3u8-files-mate/{output_id}/"
                            }
                        },
                        "Outputs": [
                            {
                                "VideoDescription": {
                                    "CodecSettings": {
                                        "Codec": "FRAME_CAPTURE",
                                        "FrameCaptureSettings": {
                                            "MaxCaptures": 2,
                                            "FramerateNumerator": 30,
                                            "FramerateDenominator": 100,
                                            "Quality": 80
                                        }
                                    },
                                    "Width": 1280,
                                    "Height": 720
                                },
                                "ContainerSettings": {
                                    "Container": "RAW"
                                },
                                "NameModifier": "poster"
                            }
                        ]
                    }
                ],
                "TimecodeConfig": {
                    "Source": "ZEROBASED"
                }
            },
            "Role": "arn:aws:iam::835898206524:role/media-convert",
            "UserMetadata": {
                "video_id": output_id
            }
        }
        response = self.media_convert_client.create_job(**output_template)
        return response['Job']['Id']

    def get_job(self, job_id: str):
        response = self.media_convert_client.get_job(Id=job_id)
        return response

    def get_job_status(self, job_id: str):
        response = self.get_job(job_id)
        return response['Job']['Status']
