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
print(response)


# upload file
with open('test.txt', 'rb') as file_contents:
    client.put_object(
        Bucket='mindjunkies',
        Key='test.txt',
        Body=file_contents,
    )

# download file
client.download_file(
    Bucket='mindjunkies',
    Key='test.txt',
    Filename='tmp/test.txt',
)
