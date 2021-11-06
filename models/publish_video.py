from pydantic import BaseModel


class PublishVideoModel(BaseModel):
    id: str
    title: str
    subreddit: str
