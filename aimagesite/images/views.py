from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import FormView
from django.views.generic import CreateView, ListView, DeleteView, DetailView
from .forms import UploadForm, UploadFromGDForm
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

from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2 import service_account

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


class ImageUploadfromGDView(LoginRequiredMixin, FormView):

    form_class = UploadFromGDForm
    template_name = "images/upload_from_gd.html"

    def get_success_url(self):
        return reverse("images:image-list", kwargs={"id": self.request.user.id})

    def form_valid(self, form):

        # url = form.data["url"]
        # check if image from url existe
        # file_id = "1sCaNcMQJslzCUym96-wNvYOpYfO0Icyg"

        name, extension = self.split_name(form.instance.name)

        file_id = form.data["file_id"]
        fobject = self.retrieve_image(file_id)
        pil_image = PILimage.open(fobject)
        django_file = self.pil_to_django(pil_image)

        self.imageModel = Image()
        self.imageModel.name = name
        self.imageModel.author = self.request.user
        self.imageModel.header_image.save(form.instance.name, django_file)
        self.imageModel.save()

        return super().form_valid(form)

    def split_name(self, name):
        splitted_name = name.split(".")
        return splitted_name[0], splitted_name[1]

    def retrieve_image(self, file_id):

        credz = {
            "type": "service_account",
            "project_id": "aimage-2020",
            "private_key_id": "5474f1bd40cb85bcce3e5c0ef1ea296bf7446695",
            "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQD3QNEOd0aYnLOG\nUTmnguMJIR6gEksDUOAMBHqp5A9uHB2ESSbfqnwy91aiXrXBpJ6que4E9H3DOQSn\nY+aEQZOQQBm4Q1c58sGkheayk2lBRzXpNt+rWSNotTp01WlfgIA+x7JGqw98awuf\noZqAa1ewZ/w0mSdB19OpfYyNk/p3zZ0rgVIbcLKkLqDp/2Zswk/Tp6sR9Y7BGcmI\nMupWI4/NxAfhEi20qKdxJ2d0H3VwF3mhiyww5WnoRXjbmDpbVa/KX0HGcpxxst0F\nDMXkU1QnxaFBQpIBNlfiLyr2LombcUX50TzpIRy3686/hw+o64tJPNOQtPAkeJMq\n3kMswE7HAgMBAAECggEAdN+YEkjyP2BPAe4yHQrjC6Uyp0KOX75icXvKibTqUEeM\n8kNr0yzwsVy2AGFZc/O/Jn9l0cTKD7ZLi15PD/Q5buXF4pI+UH995il/L6k7hyZE\nhv0vw/yKHswPmjtoqEKDHGnjzMC+PLcS0v2eHRbgZ9v3XNuKMXb2L7dPcXrh2a+T\nPB8cnHg1a7tZKhg+jp4r4euPbk0G5xj6kthNVzF0URBS+XjMiEJ7GE+RBMqSqlGO\np5FF2F8H9jkHmJyek91FEZH2SBD9w3J+oZm4ZtPxrMSqKj+w2KEuKE38PpesIKSg\n95OyuCOCmZEyPzOI2OWq0DDKWNd4AUEeRRFHvbF92QKBgQD/Tk0IW4MGoxyAMyzY\nHI+PKpIezSrLcjbF+RjJJ1vAR/rx9CO/WJhQsh6zwCm/jK1QZUho+A1FkRkZaaF3\nLSekiyJHYVxz6h8YKLs0EXVRbleTgXYJSpsS2Zbn8zXfLjDbR22EKTwYu84PLfhu\nOP7nSLKKvOUz9gJgPmgP68wEjwKBgQD37OkuP0RIEQN6GIjL0EblRLIwfO63jlZR\nNhGnT/xzcGCAu42M6h5NPpz/R9swLlc3b4nKZu/ILBxa3rfDBgTh7Nw8LbeEwyg0\n7vV3KQCGPJxYCpy/czX+lbfz+M2uBeX6FZpyO1mEPx7pMbUKU3SaZpfTC+p4QFGa\nPYEdN/HeSQKBgQC23AJYphLmwhU7zWulLm+0fy1BWnn4VcndaljSWppg0i1u9wpT\nlsUhpzJOVKiSRdQs7R478M6wsQhlJz86+OCX/f+DWLy7WUkEKMhMtuRserfHMsa0\nSPdhPO/VGmHPhGoB5NsP+ejNXlZskOSLLc+FIJCgxkL0QJPbE1e9b4olCQJ/DY7n\nMaBEG6zSg9rToFHDjsYy+HPcmi0ui0JptLyrEaUTofafxxUGkzLZYxyK4BeorV9s\nKaV3d3ryEgYcBo5Ntg09/gyB/MCvcjWfNuUHIlAuPKJX8CBc049cf/sbRGkOKp8D\n0ztrqc/J4PbW77mgptD1fJUqPWlHDShP50kn8QKBgQCauMtp4FJM9tuxWa9t88mD\npVgb8L6g7b2cTh84dLup15myzgJse2wOmTaxDhkvzr9nrRZrzjEUlKvF5a69dQFC\n6Q1l91gyGQC3SvRxYEeDX68l/IqTFFZ70QKynDSCaHohhRYl/A7004GCEGcfBFaG\nnBs2lnFEg//n/sHvj2XNYg==\n-----END PRIVATE KEY-----\n",
            "client_email": "aimage@aimage-2020.iam.gserviceaccount.com",
            "client_id": "110698585778859900855",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/aimage%40aimage-2020.iam.gserviceaccount.com",
        }
        # put json credentials her from service account or the like
        # More info: https://cloud.google.com/docs/authentication

        credentials = service_account.Credentials.from_service_account_info(credz)
        drive_service = build("drive", "v3", credentials=credentials)

        request = drive_service.files().get_media(fileId=file_id)
        fh = BytesIO()  # this can be used to keep in memory
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()

        return fh

    def pil_to_django(self, image, format="PNG"):
        fobject = BytesIO()
        image.save(fobject, format=format)
        return ContentFile(fobject.getvalue())


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
            return render(request, "images/homepage.html", {"limit_exceeded": False, "no_image":True})

        if request.user.id == None:
            w, h = get_image_dimensions(request.FILES["customFile"])
            if w > 800 or h > 600:
                return render(request, "images/homepage.html", {"limit_exceeded": True})
        else:

            image = Image.objects.create(header_image=request.FILES["customFile"])
            image.save()

            improve_image(image)

            return HttpResponseRedirect(reverse("images:image-result", args=(image.id,)))
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
