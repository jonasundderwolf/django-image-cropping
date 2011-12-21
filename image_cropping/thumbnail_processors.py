import logging


logger = logging.getLogger(__name__)

def crop_corners(image, box=None, **kwargs):
    """
    Crop corners to the selection defined by image_cropping
    """

    if box:
        try:
            values = [int(x) for x in box.split(',')]
            width = abs(values[2] - values[0])
            height = abs(values[3] - values[1])
            if width and height and (width != image.size[0] or height != image.size[1]):
                image = image.crop(values)
        except (ValueError, IndexError):
            # There's garbage in the cropping field, ignore
            logger.warning('Unable to parse "box" parameter value "%s". Ignoring.' % box)

    return image

