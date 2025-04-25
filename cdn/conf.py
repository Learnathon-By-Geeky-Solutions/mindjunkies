import os
from decouple import config

AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = "mindjunkies"
AWS_S3_ENDPOINT_URL = "https://blr1.digitaloceanspaces.com"
AWS_S3_OBJECT_PARAMETERS = {
    "CacheControl": "max-age=86400",
    "ACL": "public-read",
}
AWS_LOCATION = "https://mindjunkies.blr1.digitaloceanspaces.com"
DEFAULT_FILE_STORAGE = "mindjunkies.cdn.backends.MediaRootS3Boto3Storage"
STATICFILES_STORAGE = "mindjunkies.cdn.backends.StaticRootS3Boto3Storage"
