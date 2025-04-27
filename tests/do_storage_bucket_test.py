import boto3
from decouple import config

session = boto3.session.Session()
client = session.client(
    's3',
    region_name='blr1',
    endpoint_url='https://blr1.digitaloceanspaces.com',
    aws_access_key_id=config('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=config('AWS_SECRET_ACCESS_KEY'),
)

response = client.list_buckets()

FILE_NAME = 'test.txt'
# upload file
with open(FILE_NAME, 'rb') as file_contents:
    client.put_object(
        Bucket='mindjunkies',
        Key=FILE_NAME,
        Body=file_contents,
    )

# download file
client.download_file(
    Bucket='mindjunkies',
    Key=FILE_NAME,
    Filename='tmp/test.txt',
)
