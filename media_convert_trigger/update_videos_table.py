import boto3

dynamo_client = boto3.resource("dynamodb").Table("videos_table")


def handler(event, context):
    status = event["detail"]["status"]
    video_id = event["detail"]["userMetadata"]["video_id"]
    args = [("status", status)]
    query = ", ".join([f"#{x[0]}=:{x[0]}" for x in args])
    update_expression = f"set {query}"
    expression_attribute_values = {f":{x[0]}": x[1] for x in args}
    expression_attribute_names = {f"#{x[0]}": x[0] for x in args}
    dynamo_client.update_item(
        Key={"id": video_id},
        UpdateExpression=update_expression,
        ExpressionAttributeValues=expression_attribute_values,
        ExpressionAttributeNames=expression_attribute_names,
        ReturnValues="NONE",
    )
