from django.core.exceptions import ImproperlyConfigured
from django.utils.module_loading import import_string
from django.utils.translation import gettext as _

from .config import settings


def max_cropping(width, height, image_width, image_height, free_crop=False):
    if free_crop:
        return [0, 0, image_width, image_height]

    ratio = width / float(height)
    if image_width < image_height * ratio:
        # width fits fully, height needs to be cropped
        offset = int(round((image_height - (image_width / ratio)) / 2))
        return [0, offset, image_width, image_height - offset]

    # height fits fully, width needs to be cropped
    offset = int(round((image_width - (image_height * ratio)) / 2))
    return [offset, 0, image_width - offset, image_height]


def get_backend():
    try:
        cls = import_string(settings.IMAGE_CROPPING_BACKEND)
    except ImportError as e:
        raise ImproperlyConfigured(
            _("Can't retrieve the image backend '{}'. Message: '{}'.").format(
                settings.IMAGE_CROPPING_BACKEND, e
            )
        )

    return cls(**settings.IMAGE_CROPPING_BACKEND_PARAMS)
