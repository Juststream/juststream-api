from services.dynamodb_clients.base_dynamodb_client import DynamoClient


class RedditCommentsTable(DynamoClient):

    def __init__(self):
        super().__init__('reddit_comments_table')
