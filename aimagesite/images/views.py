from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.views.generic import CreateView, ListView, DeleteView
from .forms import UploadForm
from .models import Image
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from PIL import Image as PILimage
from urllib.request import urlopen
from io import BytesIO
from django.core.files.base import ContentFile
from django.urls import reverse
from urllib.parse import urlsplit, urlparse
import os.path
import http.client

import sys

# Create your views here.

"""
def upload(request):

    if request.method == "POST":
        form = UploadForm(request.POST)
        form.instance.author = request.user
        # save img from url TODO
        form.save()
        return redirect("http://localhost:8000/images/list/" + str(request.user.id))
    else:
        form = UploadForm()
    return render(request, "images/upload.html", {"form": form})

class ImageUploadView(LoginRequiredMixin, CreateView):

    model = Image
    template_name = "images/upload.html"
    fields = ["name", "header_image"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
"""


class ImageUploadView(LoginRequiredMixin, FormView):

    form_class = UploadForm
    template_name = "images/upload.html"

    def get_success_url(self):
        return reverse("images:image-list", kwargs={"id": self.request.user.id})

    def form_valid(self, form):
        def _invalidate(msg):
            form.errors["url"] = [
                msg,
            ]
            form.errors["header_image"] = [
                msg,
            ]
            return super(ImageUploadView, self).form_invalid(form)

        form.instance.author = self.request.user

        if "header_image" in form.data and form.data["url"]:
            url = form.data["url"]
            # check if image from url existe
            domain, path = self.split_url(url)
            if not self.image_exists(domain, path):
                return _invalidate(
                    "Couldn't retreive image. (There was an error reaching the server)"
                )

            extension = self.get_file_extension(url)
            fobject = self.retrieve_image(url)
            pil_image = PILimage.open(fobject)
            django_file = self.pil_to_django(pil_image)
            self.imageModel = Image()
            self.imageModel.name = form.instance.name
            self.imageModel.author = form.instance.author
            self.imageModel.header_image.save(
                form.instance.name + extension, django_file
            )
            self.imageModel.save()
            return super().form_valid(form)
        elif not ("header_image" in form.data) and not form.data["url"]:
            self.imageModel = Image()
            self.imageModel.name = form.instance.name
            self.imageModel.author = form.instance.author
            self.imageModel.header_image = form.instance.header_image
            self.imageModel.save()
            return super().form_valid(form)
        elif "header_image" in form.data and not form.data["url"]:
            return _invalidate("Add Image or add Url")
        else:
            return _invalidate("Add either Image or Url not both")

    def retrieve_image(self, url):
        return BytesIO(urlopen(url).read())

    def pil_to_django(self, image, format="PNG"):
        fobject = BytesIO()
        image.save(fobject, format=format)
        return ContentFile(fobject.getvalue())

    def get_file_extension(self, url):
        return os.path.splitext(os.path.basename(urlsplit(url).path))[1]

    def image_exists(self, domain, path):
        try:
            conn = http.client.HTTPConnection(domain)
            conn.request("HEAD", path)
            response = conn.getresponse()
            conn.close()
        except:
            return False
        return response.status == 200

    def split_url(self, url):
        parse_object = urlparse(url)
        return parse_object.netloc, parse_object.path


class ImageListView(LoginRequiredMixin, ListView):

    model = Image
    template_name = "images/user_images_list.html"
    context_object_name = "images"

    def get_queryset(self):
        return (
            Image.objects.filter(author=self.kwargs["id"])
            .order_by("date_posted")
            .reverse()
        )


class ImageDeleteView(LoginRequiredMixin, DeleteView):
    model = Image

    def test_func(self):
        image = self.get_object()
        if self.request.user == image.author:
            return True
        return False

    def get_success_url(self):
        image = self.get_object()
        return reverse("images:image-list", kwargs={"id": image.author_id})
