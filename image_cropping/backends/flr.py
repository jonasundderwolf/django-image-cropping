"""
Backend for django-filer

https://github.com/divio/django-filer

Usage: Subsititute FilerImageField for CroppableFilerImageField
"""

from filer.fields.image import (
    AdminImageWidget,
    AdminImageFormField, FilerImageField,
)
from filer.models import File
from easy_thumbnails.files import get_thumbnailer
from easy_thumbnails.source_generators import pil_image

from ..widgets import CropWidget
from .base import ImageBackend


class FilerCropWidget(AdminImageWidget, CropWidget):

    def render(self, name, value, attrs=None):
        if value:
            file_obj = File.objects.get(pk=value)
            attrs = attrs or {}
            attrs.update({
                'class': 'crop-thumb',
                'data-thumbnail-url':
                    file_obj.thumbnails['admin_sidebar_preview'],
                'data-field-name': name,
                'data-org-width': file_obj.width,
                'data-org-height': file_obj.height,
                'style': 'display:none',

            })
        return super(FilerCropWidget, self).render(name, value, attrs)


class CroppableFormField(AdminImageFormField):
    widget = FilerCropWidget


class CroppableFilerImageField(FilerImageField):
    default_form_class = CroppableFormField


class FilerBackend(ImageBackend):
    version_suffix = 'crop'

    WIDGETS = dict(ImageBackend.WIDGETS)
    WIDGETS['CroppableFilerImageField'] = FilerCropWidget

    def get_thumbnail_url(self, image_path, thumbnail_options):
        thumb = get_thumbnailer(image_path)
        return thumb.get_thumbnail(thumbnail_options).url

    def get_size(self, image):
        return pil_image(image).size
