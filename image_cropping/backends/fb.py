"""
Backend for filebrowser_ package. This module can't be named
"filebrowser" in order to avoid Python import conflicts.

.. _filebrowser: https://github.com/sehmaschine/django-filebrowser
"""

from django.db.models.fields.files import ImageFieldFile

from filebrowser.base import FileObject
from filebrowser.fields import FileBrowseWidget
from filebrowser.sites import site

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
        image = self.get_imageobject(image_path)
        version_suffix = thumbnail_options.pop('version_suffix', self.version_suffix)
        return image.version_generate(version_suffix, thumbnail_options).url

    def get_size(self, image):
        image = self.get_imageobject(image)
        return image.dimensions

    def get_imageobject(self, image):
        if isinstance(image, FileObject):
            return image
        if isinstance(image, ImageFieldFile):
            image = image.path
            if image.startswith(site.storage.base_location):
                image = image[len(site.storage.base_location)+1:]
        return FileObject(image)
