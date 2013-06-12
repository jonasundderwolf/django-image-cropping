import logging


logger = logging.getLogger(__name__)

def crop_corners(image, box=None, **kwargs):
    """
    Crop corners to the selection defined by image_cropping

    `box` is a string of the format 'x1,y1,x2,y1' or a four-tuple of integers.
    """
    if isinstance(box, basestring):
        if box.startswith('-'):
            pass # TBC: what does this indicate? No-op value?
        else:
            try:
                box = map(int, box.split(','))
            except (ValueError, IndexError):
                # There's garbage in the cropping field, ignore
                logger.warning(
                    'Unable to parse "box" parameter "%s". Ignoring.' % box)

    if isinstance(box, (list, tuple)):
        if len(box) == 4:
            if sum(box) < 0:
                pass # TODO: add explanatory comment for this please
            else:
                width = abs(box[2] - box[0])
                height = abs(box[3] - box[1])
                if width and height and (width, height) != image.size:
                    image = image.crop(box)
        else:
            logger.warning(
                '"box" parameter requires four values. Ignoring "%r".' % (box,)
            )

    return image

