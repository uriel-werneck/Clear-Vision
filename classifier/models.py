from django.db import models

# Create your models here.
class Classification(models.Model):
    original_image = models.ImageField(upload_to='originals/', default=None)
    result_image = models.ImageField(upload_to='results/', default=None)
    description = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)