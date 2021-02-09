from django.contrib import admin
from .models import Backups, BackupLocation


@admin.register(BackupLocation)
class BackupLocationAdmin(admin.ModelAdmin):
    list_display = ['path', 'archived']


@admin.register(Backups)
class BackupsAdmin(admin.ModelAdmin):
    list_display = ['location', 'file', 'off_site_backup_date', 'last_seen_date']
    readonly_fields = ['location', 'file', 'glacier_archive_id', 'off_site_backup_date', 'last_seen_date']
