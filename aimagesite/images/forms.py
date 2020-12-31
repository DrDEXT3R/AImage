from django import forms
from .models import Image

VALID_IMAGE_EXTENSIONS = [
    ".jpg",
    ".jpeg",
    ".png",
    ".gif",
]


class UploadForm(forms.ModelForm):

    header_image = forms.ImageField(label="Image", required=False)

    url = forms.URLField(
        required=False,
        error_messages={
            "required": "Please enter a valid URL to an image (.jpg .jpeg .png)"
        },
    )

    class Meta:
        model = Image
        fields = ["name", "header_image"]

    def clean_url(self):
        url_text = self.cleaned_data["url"].lower()
        if len(url_text) > 0:
            if not self.valid_url_extension(url_text):
                raise forms.ValidationError(
                    (
                        "Not a valid Image. The URL must have an image extensions (.jpg/.jpeg/.png)"
                    )
                )
        return url_text

    def valid_url_extension(self, url_text, extension_list=VALID_IMAGE_EXTENSIONS):
        return any([url_text.endswith(e) for e in extension_list])


class UploadFromGDForm(forms.ModelForm):

    file_id = forms.TextInput()

    class Meta:
        model = Image
        fields = ["name"]
