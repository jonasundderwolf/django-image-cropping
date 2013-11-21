from __future__ import unicode_literals
import logging

from django.db.models import get_model, ObjectDoesNotExist
from django.contrib.admin.widgets import AdminFileWidget, ForeignKeyRawIdWidget
from django.conf import settings

from easy_thumbnails.files import get_thumbnailer

logger = logging.getLogger(__name__)


def thumbnail(image_path):
    thumbnailer = get_thumbnailer(image_path)
    thumbnail_options = {
        'detail': True,
        'size': getattr(settings, 'IMAGE_CROPPING_THUMB_SIZE', (300, 300)),
    }
    thumb = thumbnailer.get_thumbnail(thumbnail_options)
    return thumb.url


def get_attrs(image, name):
    try:
        return {
            'class': "crop-thumb",
            'data-thumbnail-url': thumbnail(image),
            'data-field-name': name,
            'data-org-width': image.width,
            'data-org-height': image.height,
        }
    except ValueError:
        # can't create thumbnail from image
        return {}


class CropWidget(object):
    class Media:
        js = (
            getattr(settings, 'JQUERY_URL',
                    'https://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js'),
            "image_cropping/js/jquery.Jcrop.min.js",
            "image_cropping/image_cropping.js",
        )
        css = {'all': ("image_cropping/css/jquery.Jcrop.min.css",
                       "image_cropping/css/image_cropping.css",)}


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
                attrs.update(get_attrs(image, name))
            except ObjectDoesNotExist:
                logger.error("Can't find object: %s.%s with primary key %s "
                             "for cropping." % (app_name, model_name, value))
            except AttributeError:
                logger.error("Object %s.%s doesn't have an attribute named '%s'." % (
                    app_name, model_name, self.field_name))
        return super(CropForeignKeyWidget, self).render(name, value, attrs)
