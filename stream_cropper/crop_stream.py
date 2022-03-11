import json

import boto3
import streamlink

s3_client = boto3.client('s3')


def handler(event, context):
    headers = "User-Agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15"
    payload = event['body']
    if isinstance(payload, str):
        payload = json.loads(payload)
    stream_url = payload['stream_url']
    bytes_size = payload['bytes_size']
    output_path = payload['output_path']
    header_overrides = payload.get('header_overrides', '')
    if isinstance(header_overrides, dict):
        header_overrides = ';'.join([f'{key}={value}' for key, value in header_overrides.items()])
    if header_overrides:
        headers = header_overrides
    session = streamlink.Streamlink()
    session.set_option('http-header', headers)
    stream = session.streams(stream_url).get('best')
    fd = stream.open()
    try:
        data = fd.read(bytes_size)
        data += fd.read(bytes_size)
        data += fd.read(bytes_size)
        s3_client.put_object(
            Body=data,
            Bucket='m3u8-files-mate',
            Key=output_path
        )
    finally:
        fd.close()
    return {
        'headers': {},
        'isBase64Encoded': True,
        'statusCode': 200,
        'body': ''
    }


if __name__ == '__main__':
    handler({
        'body': {
            "stream_url": "https://tv.cdn.xsg.ge/gpb-1tv/tracks-v1a1/mono.m3u8",
            "bytes_size": 5000000,
            "output_path": "hey/mate.ts",
            "header_overrides": {}
        }
    }, {})
    print('https://d235yh2mc42dtx.cloudfront.net/hey/mate.ts')
