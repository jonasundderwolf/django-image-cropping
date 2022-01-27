from appconf import AppConf

from django.conf import settings


class ImageCroppingAppConf(AppConf):
    THUMB_SIZE = (300, 300)
    SIZE_WARNING = False
    BACKEND = "image_cropping.backends.easy_thumbs.EasyThumbnailsBackend"
    BACKEND_PARAMS = {}
    JQUERY_URL = settings.STATIC_URL + "admin/js/vendor/jquery/jquery.min.js"
