from __future__ import unicode_literals
import logging

from django import forms
try:
    from django.apps import apps
except ImportError:
    # django.apps is not available until Django 1.7
    apps = None

from django.db.models import get_model, ObjectDoesNotExist
from django.contrib.admin.widgets import AdminFileWidget, ForeignKeyRawIdWidget
from easy_thumbnails.files import get_thumbnailer
from easy_thumbnails.source_generators import pil_image
from .config import settings

logger = logging.getLogger(__name__)


def thumbnail(image_path):
    thumbnailer = get_thumbnailer(image_path)
    thumbnail_options = {
        'detail': True,
        'upscale': True,
        'size': settings.IMAGE_CROPPING_THUMB_SIZE,
    }
    thumb = thumbnailer.get_thumbnail(thumbnail_options)
    return thumb


def get_attrs(image, name):
    try:
        # TODO test case
        # If the image file has already been closed, open it
        if image.closed:
            image.open()

        # Seek to the beginning of the file.  This is necessary if the
        # image has already been read using this file handler
        image.seek(0)

        try:
            # open image and rotate according to its exif.orientation
            width, height = pil_image(image).size
        except AttributeError:
            # invalid image -> AttributeError
            width = image.width
            height = image.height
        return {
            'class': "crop-thumb",
            'data-thumbnail-url': thumbnail(image).url,
            'data-field-name': name,
            'data-org-width': width,
            'data-org-height': height,
            'data-max-width': width,
            'data-max-height': height,
        }
    except (ValueError, AttributeError, IOError):
        # can't create thumbnail from image
        return {}


_static = None

def static(path):
    if apps is None:
        # Django < 1.7 compatibility
        return path

    global _static
    if _static is None:
        if apps.is_installed('django.contrib.staticfiles'):
            from django.contrib.staticfiles.templatetags.staticfiles import static as _static
        else:
            from django.templatetags.static import static as _static
    return _static(path)


class CropWidget(object):

    def _media(self):
        js = [
            "image_cropping/js/jquery.Jcrop.min.js",
            "image_cropping/image_cropping.js",
        ]
        js = [static(path) for path in js]

        if settings.IMAGE_CROPPING_JQUERY_URL:
            js.insert(0, settings.IMAGE_CROPPING_JQUERY_URL)

        css = [
            "image_cropping/css/jquery.Jcrop.min.css",
            "image_cropping/css/image_cropping.css",
        ]
        css = {'all': [static(path) for path in css]}

        return forms.Media(css=css, js=js)

    media = property(_media)


class ImageCropWidget(AdminFileWidget, CropWidget):
    def render(self, name, value, attrs=None):
        if not attrs:
            attrs = {}
        if value:
            attrs.update(get_attrs(value, name))
        return super(AdminFileWidget, self).render(name, value, attrs)


class HiddenImageCropWidget(ImageCropWidget):
    def render(self, name, value, attrs=None):
        if not attrs:
            attrs = {}
        # we need to hide it the whole field by JS because the admin
        # doesn't yet support hidden fields:
        # https://code.djangoproject.com/ticket/11277
        attrs['data-hide-field'] = True
        return super(HiddenImageCropWidget, self).render(name, value, attrs)


class CropForeignKeyWidget(ForeignKeyRawIdWidget, CropWidget):
    def __init__(self, *args, **kwargs):
        self.field_name = kwargs.pop('field_name')
        super(CropForeignKeyWidget, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None):
        if attrs is None:
            attrs = {}

        if value:
            app_name = self.rel.to._meta.app_label
            model_name = self.rel.to._meta.object_name.lower()
            try:
                image = getattr(
                    get_model(app_name, model_name).objects.get(pk=value),
                    self.field_name,
                )
                if image:
                    attrs.update(get_attrs(image, name))
            except ObjectDoesNotExist:
                logger.error("Can't find object: %s.%s with primary key %s "
                             "for cropping." % (app_name, model_name, value))
            except AttributeError:
                logger.error("Object %s.%s doesn't have an attribute named '%s'." % (
                    app_name, model_name, self.field_name))
        return super(CropForeignKeyWidget, self).render(name, value, attrs)
