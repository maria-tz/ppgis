# mapapp/models.py
from django.db import models
import os
from django.conf import settings
from django.core.files.storage import default_storage

class Pin(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    image = models.ImageField(upload_to='pins/')  # Upload path inside 'media/pins/'

    def delete(self, *args, **kwargs):
        # Delete the image file from the file system
        if self.image:
            # Use the storage API to access the file
            if default_storage.exists(self.image.name):
                default_storage.delete(self.image.name)
        super().delete(*args, **kwargs)
