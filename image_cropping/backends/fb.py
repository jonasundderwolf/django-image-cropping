"""
Backend for filebrowser_ package. This module can't be named
"filebrowser" in order to avoid Python import conflicts.

.. _filebrowser: https://github.com/sehmaschine/django-filebrowser
"""

from filebrowser.base import FileObject
from filebrowser.fields import FileBrowseWidget

from ..widgets import CropWidget, get_attrs
from .base import ImageBackend


class CropFileBrowseWidget(FileBrowseWidget, CropWidget):
    def render(self, name, value, attrs=None):
        if not attrs:
            attrs = {}
        if value:
            attrs.update(get_attrs(value, name))

        return super(CropFileBrowseWidget, self).render(name, value, attrs)


class FileBrowserBackend(ImageBackend):
    # params
    version_suffix = 'crop'

    WIDGETS = dict(ImageBackend.WIDGETS)
    WIDGETS['FileBrowseField'] = CropFileBrowseWidget

    def get_thumbnail_url(self, image_path, thumbnail_options):
        image = image_path if isinstance(
            image_path, FileObject) else FileObject(image_path)
        return image.version_generate(self.version_suffix, thumbnail_options).url

    def get_size(self, image):
        image = image if isinstance(image, FileObject) else FileObject(image)
        return image.dimensions
