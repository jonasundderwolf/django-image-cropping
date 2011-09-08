import re
from django.utils.safestring import mark_safe
from django.contrib.admin.widgets import AdminFileWidget
from django.db.models.fields.files import FieldFile
from django.conf import settings

from easy_thumbnails.files import get_thumbnailer, Thumbnailer


ADMIN_THUMBNAIL_SIZE = getattr(settings, 'IMAGE_CROPPING_THUMB_SIZE', (300, 300))
def thumbnail(image_path):
    thumbnailer = get_thumbnailer(image_path)
    thumbnail_options = {
        'detail': True,
        'size': ADMIN_THUMBNAIL_SIZE,
    }
    thumb = thumbnailer.get_thumbnail(thumbnail_options)
    return thumb.url


class AdminCropImageWidget(AdminFileWidget):
    class Media:
        js = (
            'https://ajax.googleapis.com/ajax/libs/jquery/1.5/jquery.min.js',
            "image_cropping/jquery.imgareaselect.min.js",
            "image_cropping/image_cropping.js",
        )
        css= {'all' : ("image_cropping/imgareaselect-default.css",)}

    def render(self, name, value, attrs=None):
        output = []
        if value and (isinstance(value, FieldFile) or isinstance(value,
            Thumbnailer)):
            field_name = name

            output.append('<img src="%s" class="admin-thumb" data-field-name="%s">' % (
                thumbnail(value), field_name
            ))
        output.append(super(AdminFileWidget, self).render(name, value, attrs))
        return mark_safe(u''.join(output))
