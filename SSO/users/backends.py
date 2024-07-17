from django.core.files.storage import Storage
from google.cloud import storage
from django.conf import settings
import datetime

class GoogleDriveStorage(Storage):
    def __init__(self, *args, **kwargs):
        self.client = storage.Client()
        self.bucket_name = settings.GS_BUCKET_NAME
        self.bucket = self.client.bucket(self.bucket_name)

    def _open(self, name, mode='rb'):
        # Custom implementation to open a file
        pass

    def _save(self, name, content):
        # Custom implementation to save a file
        pass

    def url(self, name):
        # Generate a signed URL for the file
        blob = self.bucket.blob(name)
        url = blob.generate_signed_url(
            version='v4',
            expiration=datetime.timedelta(hours=1),  # URL valido per 1 ora
            method='GET'
        )
        return url

    def exists(self, name):
        # Check if the file exists
        return self.bucket.blob(name).exists()

    def delete(self, name):
        # Delete the file
        self.bucket.blob(name).delete()
