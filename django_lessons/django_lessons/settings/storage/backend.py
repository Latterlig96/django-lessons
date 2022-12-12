from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage

class StaticStorage(S3Boto3Storage):
    bucket_name = settings.AWS_S3_STATIC_BUCKET_NAME
    default_acl = 'public-read'  
    file_overwrite = False
    url_protocol = "http:"
    custom_domain = "%s/%s" %(settings.AWS_S3_LOCAL_ENDPOINT_URL, bucket_name)

class MediaStorage(S3Boto3Storage):
    bucket_name = settings.AWS_S3_MEDIA_BUCKET_NAME
    default_acl = 'public-read'  
    file_overwrite = False
    url_protocol = "http:"
    custom_domain = "%s/%s" %(settings.AWS_S3_LOCAL_ENDPOINT_URL, bucket_name)
