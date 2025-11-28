from django.db import models

# Create your models here.
class Classification(models.Model):
    original_image = models.ImageField(upload_to='originals/', default=None)
    result_image = models.ImageField(upload_to='results/', default=None)
    cracked_confidence = models.FloatField(default=0.0)
    uncracked_confidence = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)