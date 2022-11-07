from storages.backends.s3boto3 import S3Boto3Storage


class StaticStorage(S3Boto3Storage):
    location = "statics"
    default_acl = "public-read"


class PublicMediaStorage(S3Boto3Storage):
    location = "medias"
    default_acl = "public-read"
    file_overwrite = False
