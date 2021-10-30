import boto3
from botocore.exceptions import ClientError


class S3Client:

    def __init__(self, bucket):
        self.bucket = bucket
        self._s3 = boto3.client('s3')

    def upload_file(self, body: bytes, key: str, metadata=None, content_type='binary/octet-stream'):
        """
        uploads file to s3 bucket.
        Args:
            content_type: Content Type
            metadata: Meta data
            body: content of file
            key: path to s3

        Returns:
            (dict): response from S3

        """
        response = self._s3.put_object(
            Body=body,
            Bucket=self.bucket,
            Key=key,
            Metadata=metadata or {},
            ContentType=content_type
        )
        return response

    def upload_from_path(self, path: str, key: str):
        """
        Uploads file to s3 using directory path
        Args:
            path: path to local file
            key: path to s3

        Returns:
            (dict): response from S3

        """
        response = self._s3.upload_file(
            path,
            Bucket=self.bucket,
            Key=key,
        )
        return response

    def get_size(self, key: str):
        """
        Get size of file on bucket
        Args:
            key: path to s3

        Returns:
            (int): size of file

        """
        obj = self._s3.head_object(Bucket=self.bucket, Key=key)
        size = obj['ContentLength']
        return size

    def get_file(self, key: str):
        """
        Get file from S3 bucket
        Args:
            key: path to s3

        Returns:
            (str): body of file

        """
        response = self._s3.get_object(Bucket=self.bucket, Key=key)
        body = response['Body'].read()
        return body

    def exists(self, key: str):
        """
        Checks if file exists in bucket
        Args:
            key: path to s3

        Returns:
            (bool) :True if exists, otherwise False

        """

        try:
            self._s3.head_object(Bucket=self.bucket, Key=key)
        except ClientError:
            return False
        return True

    def list_objects(self, key: str):
        """
        Retrieves list of files on s3
        Args:
            key: path to s3

        Returns:
            (list): response from s3

        """
        return self._s3.list_objects(Bucket=self.bucket, Prefix=key)
