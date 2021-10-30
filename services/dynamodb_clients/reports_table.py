from services.dynamodb_clients.base_dynamodb_client import DynamoClient


class ReportsTable(DynamoClient):

    def __init__(self):
        super().__init__('reports_table', secondary_key='created_at')
