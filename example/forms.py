from django import forms

from .models import Image


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ("image_field", "cropping", "cropping_free")
