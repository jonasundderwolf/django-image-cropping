from django import template
from easy_thumbnails.files import get_thumbnailer

register = template.Library()

@register.simple_tag(takes_context=True)
def cropped(context, obj, imagefield, croppingfield):
    cropping = obj._meta.get_field(croppingfield)

    thumbnailer = get_thumbnailer(getattr(obj, imagefield))
    thumbnail_options = {
        'size': (cropping.width, cropping.height),
        'box': getattr(obj, croppingfield),
        'crop': True,
        'detail': True,
    }
    thumb = thumbnailer.get_thumbnail(thumbnail_options)

    return thumb.url

