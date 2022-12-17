from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class StaticStorage(S3Boto3Storage):
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    default_acl = 'public-read'
    file_overwrite = False
    url_protocol = 'http:'
    custom_domain = "%s/minio/%s" %(settings.AWS_S3_LOCAL_ENDPOINT, bucket_name)

class MediaStorage(S3Boto3Storage):
    bucket_name = settings.AWS_STORAGE_MEDIA_BUCKET_NAME
    default_acl = 'public-read'
    file_overwrite = False
    url_protocol = 'http:'
    custom_domain = "%s/minio/%s" %(settings.AWS_S3_LOCAL_ENDPOINT, bucket_name)
