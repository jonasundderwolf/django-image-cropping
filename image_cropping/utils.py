from easy_thumbnails.source_generators import pil_image
from easy_thumbnails.files import get_thumbnailer
from .config import settings


def thumbnail(image_path):
    thumbnailer = get_thumbnailer(image_path)
    thumbnail_options = {
        'detail': True,
        'upscale': True,
        'size': settings.IMAGE_CROPPING_THUMB_SIZE,
    }
    thumb = thumbnailer.get_thumbnail(thumbnail_options)
    return thumb


def thumbnail_attrs(image):
    try:
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
        attrs = {
            'thumb-url': thumbnail(image).url,
            'org-width': width,
            'org-height': height,
        }
        return attrs
    except (ValueError, AttributeError, IOError):
        # can't create thumbnail from image
        return None


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
