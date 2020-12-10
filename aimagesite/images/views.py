from django.shortcuts import render, redirect
from .forms import UploadForm

# Create your views here.


def upload(request):

    if request.method == "POST":
        form = UploadForm(request.POST)
        form.save()
        return redirect("homepage")
    else:
        form = UploadForm()
    return render(request, "images/upload.html", {"form": form})
