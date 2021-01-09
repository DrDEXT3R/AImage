from django.urls import path
from .views import (
    ImageUploadView,
    ImageListView,
    ImageDeleteView,
    ImageUploadfromGDView,
)
from . import views

app_name = "images"

urlpatterns = [
    path("upload/", ImageUploadView.as_view(), name="upload"),
    path("upload_from_gd/", ImageUploadfromGDView.as_view(), name="upload_from_gd"),
    path("list/<int:id>/", ImageListView.as_view(), name="image-list"),
    path("delete/<int:pk>/", ImageDeleteView.as_view(), name="image-delete"),
    # path("upload/", views.upload, name="upload"),
]
