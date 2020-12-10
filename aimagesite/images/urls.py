from django.urls import path
from .views import ImageUploadView, ImageListView
from . import views

app_name = "images"

urlpatterns = [
    path("upload/", ImageUploadView.as_view(), name="upload"),
    path("list/<int:id>/", ImageListView.as_view(), name="image-list"),
    # path("upload/", views.upload, name="upload"),
]
