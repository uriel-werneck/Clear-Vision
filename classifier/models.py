from django.db import models

# Create your models here.
class Classification(models.Model):
    image = models.ImageField(upload_to='results/')
    result = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)