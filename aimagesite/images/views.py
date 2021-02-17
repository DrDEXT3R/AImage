from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import FormView
from django.views.generic import CreateView, ListView, DeleteView, DetailView
from .forms import UploadForm
from .models import Image
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from PIL import Image as PILimage
from urllib.request import urlopen
from io import BytesIO
from django.core.files.base import ContentFile
from django.urls import reverse
from urllib.parse import urlsplit, urlparse
from django.http import HttpResponse, HttpResponseRedirect
import os.path
from django.core.files.images import get_image_dimensions
import http.client
import shutil
import subprocess
import sys


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

        requested_orderby_column = self.request.GET.get("order_by")
        if requested_orderby_column:
            order_by = requested_orderby_column
        else:
            order_by = "date_posted"

        requested_sort = self.request.GET.get("sort")

        if requested_sort == "asc":
            return Image.objects.filter(author=self.kwargs["id"]).order_by(order_by)
        elif requested_sort == "desc":
            return (
                Image.objects.filter(author=self.kwargs["id"])
                .order_by(order_by)
                .reverse()
            )
        else:
            return (
                Image.objects.filter(author=self.kwargs["id"])
                .order_by(order_by)
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


class ImageImproveView(DetailView):
    model = Image
    template_name = "images/image_improvement.html"

    def test_func(self):
        image = self.get_object()
        if self.request.user == image.author:
            return True
        return False

    def get_success_url(self):
        image = self.get_object()
        return reverse("images:image-list", kwargs={"id": image.author_id})


def like(request, image_id):

    image = get_object_or_404(Image, pk=image_id)
    image.feedback = 1
    image.save()

    return HttpResponseRedirect(reverse("images:image-list", args=(request.user.id,)))


def dislike(request, image_id):

    image = get_object_or_404(Image, pk=image_id)
    image.feedback = 0
    image.save()

    return HttpResponseRedirect(reverse("images:image-list", args=(request.user.id,)))


def upload_and_improve(request):
    if request.method == "POST":

        if len(request.FILES) == 0:
            return render(
                request,
                "images/homepage.html",
                {"limit_exceeded": False, "no_image": True},
            )

        if request.user.id == None:
            w, h = get_image_dimensions(request.FILES["customFile"])
            if w > 800 or h > 600:
                return render(request, "images/homepage.html", {"limit_exceeded": True})
        else:

            image = Image.objects.create(header_image=request.FILES["customFile"])
            image.save()

            improve_image(image)

            return HttpResponseRedirect(
                reverse("images:image-result", args=(image.id,))
            )
    else:
        return render(request, "images/homepage.html", {"limit_exceeded": False})


def improve(request, image_id):

    image = get_object_or_404(Image, pk=image_id)

    improve_image(image)

    return HttpResponseRedirect(reverse("images:image-result", args=(image.id,)))


def improve_image(image):

    filename = os.path.split(image.header_image.url)[1]
    img_dir_path = os.path.join(
        os.path.split(os.path.abspath(os.path.dirname(__file__)))[0], "media/ImagesDB"
    )
    filepath = os.path.join(img_dir_path, filename)

    if not image.improved_image:
        command = "docker run --rm -v {}:/ne/input alexjc/neural-enhance --zoom=2 input/{}".format(
            img_dir_path, filename
        )
        subprocess.Popen(command, shell=True, stdout=False)

    improved_image_filepath = os.path.join(img_dir_path, filename)

    extension = image.header_image.url.split(".")[1]
    image.improved_image = image.header_image.url.replace(
        "." + extension, "_ne2x.png"
    ).replace("/media/", "")
    image.save()
