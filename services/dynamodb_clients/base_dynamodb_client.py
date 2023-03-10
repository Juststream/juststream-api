from typing import List

import boto3
from boto3.dynamodb.conditions import Key


class DynamoClient:
    """
    Client for Dynamo DB
    """

    def __init__(self, table_name: str, primary_key="id", secondary_key=None):
        self.table_name = table_name
        self.primary_key = primary_key
        self.secondary_key = secondary_key
        self.table = boto3.resource("dynamodb", region_name="us-east-1").Table(
            self.table_name
        )

    def put_item(self, item: dict):
        """
        Puts item in dynamodb
        Args:
            item: item to insert

        Returns:
            AWS response
        """
        self.table.put_item(Item=item)
        return item

    def batch_write(self, items: list, override=False):
        """
        Puts list of items in DB
        Args:
            override: Override data if exists
            items: list of items

        Returns:
            None
        """
        if override:
            batch_writer = self.table.batch_writer(
                overwrite_by_pkeys=[self.primary_key]
            )
        else:
            batch_writer = self.table.batch_writer()
        with batch_writer as batch:
            for item in items:
                batch.put_item(Item=item)

    def get_item(self, _id: str, secondary_key: str = None) -> dict:
        """
        Returns item by id.
        Args:
            _id: Primary key of item
            secondary_key: Secondary key of item

        Returns:
            Item if found else None

        """
        keys = {self.primary_key: _id}
        if self.secondary_key:
            keys[self.secondary_key] = secondary_key
        response = self.table.get_item(Key=keys)
        return response.get("Item") or {}

    def get_all_items_by_id(self, _id: str) -> dict:
        response = self.table.query(
            KeyConditionExpression=Key(self.primary_key).eq(_id)
        )
        return response.get("Items")

    def delete_item(self, _id: str, secondary_key: str = None) -> dict:
        """
        Deletes item by id.
        Args:
            secondary_key: Secondary Key
            _id: Primary key of item

        Returns:
            Response from aws

        """
        keys = {self.primary_key: _id}
        if self.secondary_key:
            keys[self.secondary_key] = secondary_key
        response = self.table.delete_item(Key=keys)
        return response

    def update_item(
        self, _id: str, args: List[tuple], return_values: str = "ALL_NEW"
    ) -> dict:
        """
        Updates item in Dynamo DB, creates if not exists.
        Args:
            _id: Primary key of item
            args: list of arguments, first element - name, second element - value.
            return_values: which part of updated items to be returned.

        Returns:
            Updated item if found, else newly created item.

        """
        query = ", ".join(
            [f"#{x[0]}=:{x[0]}" for x in args]
        )  # Creating structure Dynamo DB asks for
        update_expression = f"set {query}"
        expression_attribute_values = {f":{x[0]}": x[1] for x in args}
        expression_attribute_names = {f"#{x[0]}": x[0] for x in args}
        response = self.table.update_item(
            Key={self.primary_key: _id},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ExpressionAttributeNames=expression_attribute_names,
            ReturnValues=return_values,
        )
        return response.get("Attributes")

    def get_all_items(self) -> list:
        """
        Retrieves all items from table

        Returns:
            All items from dynamodb table

        """
        response = self.table.scan()
        yield from response["Items"]
        while "LastEvaluatedKey" in response:
            response = self.table.scan(ExclusiveStartKey=response["LastEvaluatedKey"])
            yield from response["Items"]
