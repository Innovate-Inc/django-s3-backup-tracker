from django.db import models
import boto3
from django.conf import settings
from datetime import datetime
from pytz import UTC
from storages.backends.s3boto3 import S3Boto3Storage


class BackupLocation(models.Model):
    path = models.CharField(max_length=255)
    archived = models.BooleanField('Archived (Never Delete from AWS)', default=False)

    def __str__(self):
        return self.path


class Backups(models.Model):
    location = models.ForeignKey('BackupLocation', on_delete=models.CASCADE)
    archived = models.BooleanField('Archived (Do Not Delete from AWS)', default=False)
    file = models.FileField(max_length=255, storage=S3Boto3Storage(location='backups'))
    glacier_archive_id = models.CharField(max_length=500, blank=True, null=True)
    off_site_backup_date = models.DateTimeField(blank=True, null=True)
    last_seen_date = models.DateTimeField()

    # delete s3 file when model record is deleted
    def delete(self, *args, **kwargs):
        self.file.delete()
        super().delete(*args, **kwargs)

    # keeping in case we need to support s3 and glacier
    # def backup_to_aws_glacier(self):
    #     glacier = boto3.client('glacier',
    #                            aws_access_key_id=aws_access_key_id,
    #                            aws_secret_access_key=aws_secret_access_key,
    #                            region_name=aws_region_name)
    #     with open(r'{}\{}'.format(self.location.path, self.filename), 'rb') as file:
    #         response = glacier.upload_archive(vaultName=AWS_VAULT, archiveDescription=self.filename, body=file)
    #         self.glacier_archive_id = response['archiveId']
    #         self.off_site_backup_date = datetime.utcnow().replace(tzinfo=UTC)
    #         self.save()
    #
    # def delete_aws_glacier_archive(self):
    #     glacier = boto3.client('glacier',
    #                            aws_access_key_id=aws_access_key_id,
    #                            aws_secret_access_key=aws_secret_access_key,
    #                            region_name=aws_region_name)
    #     response = glacier.delete_archive(vaultName=AWS_VAULT, archiveId=self.glacier_archive_id)
    #     if response['ResponseMetadata']['HTTPStatusCode'] == 204:
    #         self.delete()
