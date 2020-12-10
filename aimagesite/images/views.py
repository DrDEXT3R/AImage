from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView
from .forms import UploadForm
from .models import Image
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.


def upload(request):

    if request.method == "POST":
        form = UploadForm(request.POST)
        form.instance.author = request.user
        form.save()
        return redirect("homepage")
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


class ImageListView(LoginRequiredMixin, ListView):

    model = Image
    template_name = "images/user_images_list.html"
    context_object_name = "images"
    ordering = ["-date_posted"]

    def get_queryset(self):
        return Image.objects.filter(author=self.kwargs["id"])
