from django import template
from django.conf import settings

from ..utils import get_backend

register = template.Library()
VALID_OPTIONS = ("scale", "width", "height", "max_size")


@register.simple_tag(takes_context=True)
def cropped_thumbnail(context, instance, ratiofieldname, **kwargs):
    """
    Syntax:
    {% cropped_thumbnail instancename "ratiofieldname"
        [scale=0.1|width=100|height=200|max_size="100x200"] [upscale=True] %}
    """

    ratiofield = instance._meta.get_field(ratiofieldname)
    image = getattr(instance, ratiofield.image_field)  # get imagefield
    if ratiofield.image_fk_field:  # image is ForeignKey
        # get the imagefield
        image = getattr(image, ratiofield.image_fk_field)

    if not image:
        return

    box = getattr(instance, ratiofieldname)
    if ratiofield.free_crop:
        if not box:
            size = (image.width, image.height)
        else:
            box_values = list(map(int, box.split(",")))
            size = (box_values[2] - box_values[0], box_values[3] - box_values[1])
    else:
        size = (int(ratiofield.width), int(ratiofield.height))

    if sum(k in kwargs for k in VALID_OPTIONS) > 1:
        raise template.TemplateSyntaxError("Only one size modifier is allowed.")

    if "scale" in kwargs:
        width = size[0] * kwargs["scale"]
        height = size[1] * kwargs["scale"]
    elif "width" in kwargs:
        width = kwargs["width"]
        height = size[1] * width / size[0]
    elif "height" in kwargs:
        height = kwargs["height"]
        width = height * size[0] / size[1]
    elif "max_size" in kwargs:
        try:
            max_width, max_height = list(map(int, kwargs["max_size"].split("x")))
        except (ValueError, AttributeError):
            raise template.TemplateSyntaxError("max_size must match INTxINT")

        width, height = size
        # recalculate height if needed
        if max_width < width:
            height = height * max_width / width
            width = max_width
        # recalculate width if needed
        if max_height < height:
            width = max_height * width / height
            height = max_height

    if any(k in kwargs for k in VALID_OPTIONS):
        # adjust size based on given modifier
        size = (int(width), int(height))

    if ratiofield.adapt_rotation:
        if (image.height > image.width) != (size[1] > size[0]):
            # box needs rotation
            size = (size[1], size[0])

    thumbnail_options = {
        "size": size,
        "box": box,
        "crop": True,
        "detail": kwargs.pop("detail", True),
        "upscale": kwargs.pop("upscale", False),
    }
    # remove all cropping kwargs
    for k in VALID_OPTIONS:
        kwargs.pop(k, None)
    # pass remaining arguments to easy_thumbnail
    thumbnail_options.update(kwargs)

    backend = get_backend()
    try:
        url = backend.get_thumbnail_url(image, thumbnail_options)
    except backend.exceptions_to_catch:
        # only raise an exception if THUMBNAIL_DEBUG is set to `True`
        if getattr(settings, "THUMBNAIL_DEBUG", False):
            raise
        else:
            url = ""
    return url
