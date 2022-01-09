import os
import time

from controllers.videos_controller import VideosController

CLIPS_DIR = 'clips'

CLIPS_SET = set()

videos_controller = VideosController()

if __name__ == '__main__':
    for clip_name in os.listdir(CLIPS_DIR):
        CLIPS_SET.add(clip_name)
    while True:
        for clip_name in os.listdir(CLIPS_DIR):
            if clip_name not in CLIPS_SET:
                CLIPS_SET.add(clip_name)
                clip_path = os.path.join(CLIPS_DIR, clip_name)
                video_item = videos_controller.upload_video_from_path(clip_path)
                print(video_item)
        time.sleep(0.1)
