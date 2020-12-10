from django import forms
from .models import Image


class UploadForm(forms.ModelForm):
    name = forms.CharField(max_length=100)

    class Meta:
        model = Image
        fields = ["name"]
