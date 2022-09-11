import sys
import time
from threading import Thread

from helpers.datetime_helper import get_current_timestamp
from helpers.match_helper import generate_match_id
from helpers.url_helper import get_website_host
from services.downloaders.video_downloader import VideoDownloader
from services.dynamodb_clients.videos_table import VideosTable
from services.media_convert_service import MediaConvertClient
from services.random_name_service import get_random_name
from services.reddit_service import RedditClient
from services.s3_clients.video_store_s3 import VideoStoreS3

video_store_s3 = VideoStoreS3()
videos_table = VideosTable()
media_convert_client = MediaConvertClient()


def reply_comment(comment):
    if comment.author != 'AutoModerator':
        return
    submission = comment.submission
    if submission.is_video:
        video_url = submission.shortlink
    else:
        video_url = submission.url
    print(video_url, 'found', flush=True)
    host = get_website_host(video_url)
    print(host, flush=True)
    if host == 'youtube.com' or host == 'youtu.be' or host == 'redd.it' or host == 'reddit.com':
        return
    elif host == 'streamable.com':
        time.sleep(15)
    elif host == 'streamwo.com':
        time.sleep(45)
    elif host == 'streamgg.com':
        time.sleep(45)
    elif host == 'v.fodder.gg':
        time.sleep(45)
    elif host == 'mixture.gg':
        time.sleep(45)
    elif host == 'clip.dubz.co':
        time.sleep(45)
    elif host == 'dubz.co':
        time.sleep(45)
    elif host == 'streamja.com':
        time.sleep(15)
    elif host == 'streamye.com':
        time.sleep(15)
    elif host == 'streamff.com':
        time.sleep(15)
    try:
        print('start downloading', flush=True)
        file = VideoDownloader(video_url).get_video_content()
    except Exception:
        print('failed', flush=True)
        return
    if not file:
        print('no file', flush=True)
        return
    file_size = sys.getsizeof(file)
    if file_size < 500000:  # 500 KB
        print('undersize')
        return
    if file_size > 1000000000:  # 100 MB
        print('oversize')
        return
    print('true', flush=True)
    video_id = get_random_name()
    print(video_id, flush=True)
    filepath = f'{video_id}/video.mp4'
    video_store_s3.upload_file(file, filepath)
    print('uploaded', flush=True)
    job_id = media_convert_client.create_streaming_videos([f's3://m3u8-files-mate/{filepath}'], video_id)
    print('created streaming videos', flush=True)
    item_to_put = {
        'id': video_id,
        'media_convert_job_id': job_id,
        'views': 1,
        'created_at': get_current_timestamp(),
        'status': 'SUBMITTED',
        'video_title': submission.title,
        'reddit_submission_id': submission.id
    }
    match_id = generate_match_id(submission.title)
    if match_id:
        item_to_put['match_id'] = match_id
    videos_table.put_item(
        item_to_put
    )
    print(f'https://juststream.live/{video_id}', 'generated', flush=True)
    print(submission.shortlink, 'Commented', flush=True)
    reddit_client.reply_comment(
        comment.id,
        f"[Juststream Mirror](https://juststream.live/{video_id})\nJuststream needs your help. From 1 October We Will NOT Be able to pay for the costs of AWS servers.\nYou can [DONATE here](https://www.buymeacoffee.com/bersena) 1 Donation (5$) can make Juststream last one more day."
    )


if __name__ == "__main__":
    subreddit = sys.argv[1]

    reddit_client = RedditClient('juststream')
    while True:
        try:
            for comment in reddit_client.reddit.subreddit(subreddit).stream.comments(skip_existing=True):
                Thread(target=reply_comment, args=(comment,)).start()
        except Exception as ex:
            print(ex, flush=True)
            continue
