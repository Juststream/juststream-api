from threading import Thread

from praw.models.util import stream_generator

from helpers.match_helper import generate_match_id
from services.dynamodb_clients.videos_table import VideosTable
from services.reddit_service import RedditClient

videos_table = VideosTable()


def update_video(submission):
    video_id = submission.url.split("juststream.live/")
    if len(video_id) > 1:
        video_id = video_id[1].split("/")[0].split("?")[0]
    else:
        return
    video_item = videos_table.get_item(video_id)
    if not video_item or video_item.get("reddit_submission_id"):
        return

    item_to_update = [
        ("reddit_submission_id", submission.id),
        ("video_title", submission.title),
    ]
    match_id = generate_match_id(submission.title)
    if match_id:
        item_to_update.append(("match_id", generate_match_id(submission.title)))
    videos_table.update_item(video_id, item_to_update)
    print(video_item, "updated", flush=True)


if __name__ == "__main__":
    reddit_client = RedditClient("juststream")
    while True:
        try:
            my_domain = reddit_client.reddit.domain("juststream.live").new
            for submission in stream_generator(my_domain, skip_existing=True):
                Thread(target=update_video, args=(submission,)).start()
        except Exception as ex:
            print(ex, flush=True)
            continue
