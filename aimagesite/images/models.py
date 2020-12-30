from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.


class Image(models.Model):
    name = models.CharField("Name", max_length=10)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)
    header_image = models.ImageField("Image", null=True, upload_to="ImagesDB/")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("images:image-list", kwargs={"id": self.author_id})
