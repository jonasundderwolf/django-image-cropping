from __future__ import unicode_literals
import logging

from django.forms import TextInput
from .config import settings

logger = logging.getLogger(__name__)


class RatioWidget(TextInput):
    class Media:
        js = (
            settings.IMAGE_CROPPING_JQUERY_URL,
            "image_cropping/js/jquery.Jcrop.min.js",
            "image_cropping/image_cropping.js",
        )
        css = {'all': ("image_cropping/css/jquery.Jcrop.min.css",
                       "image_cropping/css/image_cropping.css",)}
