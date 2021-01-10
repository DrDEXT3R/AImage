from django.urls import path
from .views import (
    ImageUploadView,
    ImageListView,
    ImageDeleteView,
    ImageUploadfromGDView,
    ImageImproveView
)
from . import views

app_name = "images"

urlpatterns = [
    path("upload/", ImageUploadView.as_view(), name="upload"),
    path("upload_from_gd/", ImageUploadfromGDView.as_view(), name="upload_from_gd"),
    path("list/<int:id>/", ImageListView.as_view(), name="image-list"),
    path("delete/<int:pk>/", ImageDeleteView.as_view(), name="image-delete"),
    path("", views.upload_and_improve, name="upload-and-improve"),
    path("<int:image_id>/improve/", views.upload_and_improve, name='improve'),
    path("improve/<int:pk>/", ImageImproveView.as_view(), name="image-result"),
    path("<int:image_id>/like", views.like, name="like"),
    path("<int:image_id>/dislike", views.dislike, name="dislike"),
]
