from appconf import AppConf

from django.conf import settings


class ImageCroppingAppConf(AppConf):
    JQUERY_URL = 'https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js'
    THUMB_SIZE = (300, 300)
    SIZE_WARNING = False
    BACKEND = 'image_cropping.backends.easy_thumbs.EasyThumbnailsBackend'
    BACKEND_PARAMS = {}
