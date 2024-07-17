from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Photo

@receiver(post_delete, sender=Photo)
def delete_file_from_gdrive(sender, instance, **kwargs):
    instance.filedata.delete(False)