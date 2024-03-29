from fastapi import APIRouter

from models.publish_video import PublishVideoModel
from services.dynamodb_clients.reddit_comments_table import RedditCommentsTable
from services.dynamodb_clients.videos_table import VideosTable
from services.reddit_service import RedditClient

router = APIRouter(prefix="/reddit")

reddit_comments_client = RedditClient("comments")
reddit_post_publish_client = RedditClient("juststream")
reddit_comments_table = RedditCommentsTable()
videos_table = VideosTable()


@router.get("/{video_id}")
def get_top_comments(video_id: str):
    video = videos_table.get_item(video_id)
    submission_id = video.get("reddit_submission_id")
    if not submission_id:
        return []
    if video["views"] < 6 or video["views"] % 10 == 0:
        best_comments = reddit_comments_client.get_best_comments(submission_id)
        if not reddit_comments_table.get_item(submission_id):
            reddit_comments_table.put_item(
                {"id": submission_id, "comments": best_comments}
            )
        else:
            reddit_comments_table.update_item(
                submission_id, [("comments", best_comments)]
            )
    else:
        best_comments = (
            reddit_comments_table.get_item(submission_id).get("comments") or []
        )

    return best_comments


@router.post("/publish")
def publish_video(publish_video_model: PublishVideoModel):
    url = "https://juststream.live/" + publish_video_model.id
    reddit_post_publish_client.post_url(
        publish_video_model.subreddit, publish_video_model.title, url
    )
    return {"status": "OK"}
