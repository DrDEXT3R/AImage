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
"""


class ImageUploadView(LoginRequiredMixin, CreateView):

    model = Image
    template_name = "images/upload.html"
    fields = ["name", "header_image"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


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
