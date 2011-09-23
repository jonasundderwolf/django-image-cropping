from django.contrib.admin.widgets import AdminFileWidget
from django.conf import settings

from easy_thumbnails.files import get_thumbnailer


ADMIN_THUMBNAIL_SIZE = getattr(settings, 'IMAGE_CROPPING_THUMB_SIZE', (300, 300))
def thumbnail(image_path):
    thumbnailer = get_thumbnailer(image_path)
    thumbnail_options = {
        'detail': True,
        'size': ADMIN_THUMBNAIL_SIZE,
    }
    thumb = thumbnailer.get_thumbnail(thumbnail_options)
    return thumb.url


class ImageCropWidget(AdminFileWidget):
    def render(self, name, value, attrs=None):
        if not attrs:
            attrs = {}
        if value:
            attrs.update({
                'class': "crop-thumb",
                'data-thumbnail-url': thumbnail(value),
                'data-field-name': name,
                'data-org-width': value.width,
                'data-org-height': value.height,
            })
        return super(AdminFileWidget, self).render(name, value, attrs)

    class Media:
        js = (
            getattr(settings, 'JQUERY_URL',
                'https://ajax.googleapis.com/ajax/libs/jquery/1.5/jquery.min.js'),
            "image_cropping/jquery.imgareaselect.min.js",
            "image_cropping/image_cropping.js",
        )
        css= {'all' : ("image_cropping/imgareaselect-default.css",)}

