from django.core.management import BaseCommand
from django.conf import settings
import os
from backups.models import Backups, BackupLocation
from datetime import timedelta
from django.utils import timezone
from django.core.files import File


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            for BACKUPS_LOCATION, location_pk in BackupLocation.objects.all().values_list('path', 'pk'):
                for file in (f for f in os.listdir(BACKUPS_LOCATION) if os.path.isfile(os.path.join(BACKUPS_LOCATION, f))):
                    backup, created = Backups.objects.update_or_create(location__path=BACKUPS_LOCATION, filename=file, defaults={
                        'location_id': location_pk,
                        'last_seen_date': timezone.now()
                    })
                    if not settings.DEBUG and created:
                        with open(file, 'rb+') as f:
                            f = File(f)
                            backup.file.save(f)

            if not settings.DEBUG:
                latest_backup_date = Backups.objects.all().latest('off_site_backup_date').off_site_backup_date - timedelta(days=93)
                last_month = timezone.now() - timedelta(days=30)
                for file in Backups.objects.exclude(archived=True, location__archived=True).filter(off_site_backup_date__lt=latest_backup_date):
                    if file.last_seen_date < last_month:
                        file.delete_aws_glacier_archive()
        except Exception as e:
            print(e)
