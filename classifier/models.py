from django.db import models
import os

# Create your models here.
class Classification(models.Model):
    original_image = models.ImageField(upload_to='originals/', default=None)
    result_image = models.ImageField(upload_to='results/', default=None)
    cracked_confidence = models.FloatField(default=0.0)
    uncracked_confidence = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)

    def delete(self, *args, **kwargs):
        if self.original_image and os.path.isfile(self.original_image.path):
            os.remove(self.original_image.path)
        if self.result_image and os.path.isfile(self.result_image.path):
            os.remove(self.result_image.path)
        super().delete(*args, **kwargs)