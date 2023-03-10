import praw


class RedditClient:
    def __init__(self, settings_id: str):
        self.reddit = praw.Reddit(settings_id)

    def reply_comment(self, comment_id: str, reply_text: str):
        return self.reddit.comment(id=comment_id).reply(reply_text)

    def get_best_comments(self, submission_id: str):
        comments = []
        submission = self.reddit.submission(submission_id)
        submission.comment_sort = "best"
        submission.comment_limit = 100
        for comment in submission.comments:
            if isinstance(comment, praw.models.MoreComments):
                continue
            if comment.author.name == "AutoModerator":
                continue
            flair = None
            if comment.author_flair_richtext:
                flair = comment.author_flair_richtext[0].get("u")
            comments.append(
                {
                    "body": comment.body,
                    "author": comment.author.name,
                    "score": comment.score,
                    "flair": flair,
                }
            )
            if len(comments) == 20:
                break
        return comments

    def post_url(self, subreddit_name, title, url):
        subreddit = self.reddit.subreddit(subreddit_name)
        subreddit.submit(title, url=url)
