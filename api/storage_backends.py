from storages.backends.s3boto3 import S3Boto3Storage


class StaticStorage(S3Boto3Storage):
    location = 'setarift/static'
    default_acl = 'public-read'


class PublicMediaStorage(S3Boto3Storage):
    location = 'setarify/media'
    default_acl = 'public-read'
    file_overwrite = False

    @property
    def querystring_auth(self):
        return False

class PrivateMediaStorage(S3Boto3Storage):
    location = 'setarify/private'
    default_acl = 'private'
    file_overwrite = False
    custom_domain = False

    @property
    def querystring_auth(self):
        return True
