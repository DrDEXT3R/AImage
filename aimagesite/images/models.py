from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Image(models.Model):
    name = models.CharField("Name", max_length=20, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    date_posted = models.DateTimeField(default=timezone.now)
    header_image = models.ImageField("Image", null=True, upload_to="ImagesDB/")
    improved_image = models.ImageField("Image", null=True, upload_to="ImagesDB/", blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("images:image-list", kwargs={"id": self.author_id})
