from helpers.datetime_helper import (
    get_hours_before_timestamp,
    get_hours_after_timestamp,
)
from services.dynamodb_clients.base_dynamodb_client import DynamoClient


class VideosTable(DynamoClient):
    def __init__(self):
        super().__init__("videos_table")

    def get_all_time_top(self):
        response = self.table.query(
            TableName=self.table_name,
            KeyConditionExpression="#status=:status",
            ExpressionAttributeValues={":status": "COMPLETE"},
            ExpressionAttributeNames={"#status": "status"},
            IndexName="status-views-index",
            Limit=6,
            ScanIndexForward=False,
        )
        return response["Items"]

    def get_items_by_match_id(self, match_id: str, timestamp: str):
        response = self.table.query(
            TableName=self.table_name,
            KeyConditionExpression="#match_id=:match_id AND #created_at BETWEEN :start_time AND :end_time",
            ExpressionAttributeValues={
                ":match_id": match_id,
                ":start_time": get_hours_before_timestamp(timestamp, 3),
                ":end_time": get_hours_after_timestamp(timestamp, 3),
            },
            ExpressionAttributeNames={
                "#match_id": "match_id",
                "#created_at": "created_at",
            },
            IndexName="match_id-created_at-index",
            Limit=15,
            ScanIndexForward=False,
        )
        return response["Items"]

    def increment_views(self, video_id: str):
        return self.table.update_item(
            Key={self.primary_key: video_id},
            ExpressionAttributeValues={":inc": 1},
            ExpressionAttributeNames={"#views": "views"},
            UpdateExpression="ADD #views :inc",
            ReturnValues="ALL_NEW",
        ).get("Attributes")


if __name__ == "__main__":
    VideosTable().update_item(
        "WoollensCarnivalsPlaited",
        [
            ("match_id", "bologna-milan"),
            ("video_title", "Roberto Soriano (Bologna) red card against Milan 58' VAR"),
        ],
    )
