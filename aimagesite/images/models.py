from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.


class Image(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)
    # header_image = models.ImageField(upload_to="ImagesDB/")
