import os
import logging

from django.db import models
from django.dispatch import receiver


logger = logging.getLogger(__name__)


class VideoFile(models.Model):
    title = models.CharField(max_length=128)
    mime_type = models.CharField(max_length=64)
    date_taken = models.DateField('date taken', null=True)
    upload_date = models.DateTimeField('date uploaded', auto_now_add=True)
    thumbnail = models.ImageField(upload_to='thumbs/', null=True)
    file_obj = models.FileField(upload_to='videos/')


    def __str__(self):
        sz = bytes_to_human_readable(self.file_obj.size)
        return f'[VideoFile] {self.title} ({sz})'


@receiver(models.signals.post_delete, sender=VideoFile)
def auto_delete_file_on_db_delete(sender, instance, **kwargs):
    """Deletes file from filesystem when corresponding
    DB object is dropped"""
    if instance.file_obj:
        if os.path.isfile(instance.file_obj.path):
            os.remove(instance.file_obj.path)
    if instance.thumbnail:
        if os.path.isfile(instance.thumbnail.path):
            os.remove(instance.thumbnail.path)


@receiver(models.signals.pre_save, sender=VideoFile)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """Deletes previous version of file from file system
    when the corresponding VideoFile is modified."""
    if not instance.pk:
        return False
    try:
        record = VideoFile.objects.get(pk=instance.pk)
        old_file = record.file_obj
        old_thumb = record.thumbnail

        new_file = instance.file_obj
        new_thumb = instance.thumbnail

        if not old_file == new_file:
            if os.path.isfile(old_file.path):
                os.remove(old_file.path)
        if not old_thumb == new_thumb:
            if os.path.isfile(old_thumb.path):
                os.remove(old_thumb.path)
    except Exception:
        return False


def bytes_to_human_readable(size):
    p = 2**10
    n = 0
    labels = ['', 'KB', 'MB', 'GB', 'TB']
    while size > p and n < len(labels):
        size /= p
        n += 1
    return f'{round(size, 1)} {labels[n]}'