from services.dynamodb_clients.base_dynamodb_client import DynamoClient


class BlogsTable(DynamoClient):

    def __init__(self):
        super().__init__('blogs_table')
