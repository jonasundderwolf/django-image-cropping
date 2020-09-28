import logging

logger = logging.getLogger(__name__)


def crop_corners(image, box=None, **kwargs):
    """
    Crop corners to the selection defined by image_cropping

    `box` is a string of the format 'x1,y1,x2,y2' or a four-tuple of integers.
    """
    if not box:
        return image

    if not isinstance(box, (list, tuple)):
        # convert cropping string to a list of integers if necessary
        try:
            box = list(map(int, box.split(",")))
        except (ValueError, AttributeError):
            # there's garbage in the cropping field, ignore
            logger.warning('Unable to parse "box" parameter "%s". Ignoring.' % box)
            box = []

    if len(box) == 4:
        if box[0] < 0:
            # a negative first box value indicates that cropping is disabled
            return image
        width = abs(box[2] - box[0])
        height = abs(box[3] - box[1])
        if width and height and (width, height) != image.size:
            image = image.crop(box)
    else:
        logger.warning('"box" parameter requires four values. Ignoring "%r".' % box)
    return image
