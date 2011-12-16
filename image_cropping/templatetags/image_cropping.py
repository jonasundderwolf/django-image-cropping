from django import template
from easy_thumbnails.files import get_thumbnailer

register = template.Library()

# Sytanx:
# {% cropped2 instancename ratiofieldname [scale=0.1|width=100|height=200] %}
@register.tag
def cropped2(parser, token):
    args = token.split_contents()

    if len(args) < 3:
        raise template.TemplateSyntaxError("%r tag requires exactly two arguments" % args[0])
    if len(args) > 4:
        raise template.TemplateSyntaxError("%r tag allows only one optional argument" % args[0])

    try:
        name, value = args[3].split('=')
        option = (name.lower(), float(value))
        if not option[0] in ('scale', 'width', 'height'):
            raise template.TemplateSyntaxError("invalid optional argument %s" % args[3])
        if option[1] < 0:
            raise template.TemplateSyntaxError("%s must have a positive value" % option[0])

    except ValueError:
        raise template.TemplateSyntaxError("%s needs an numeric argument" % args[3])
    except IndexError:
        option = None

    return CroppingNode(args[1], args[2], option)

class CroppingNode(template.Node):
    def __init__(self, instance, ratiofieldname, option=None):
        self.instance = instance
        self.ratiofieldname = ratiofieldname
        self.option = option

    def render(self, context):
        instance = template.Variable(self.instance).resolve(context)
        ratiofield =instance._meta.get_field(self.ratiofieldname)
        image = getattr(instance, ratiofield.image_field)
        size = (int(ratiofield.width), int(ratiofield.height))
        box = getattr(instance, self.ratiofieldname)

        option = self.option
        if option:
            if option[0] == 'scale':
                width = size[0] * option[1]
                height = size[1] * option[1]
            elif option[0] == 'width':
                width = option[1]
                height = size[1] * width / size[0]
            elif option[0] == 'height':
                height = option[1]
                width = height * size[0] / size[1]
            size = (int(width), int(height))

        thumbnailer = get_thumbnailer(image)
        # TODO force upscaling if requested
        thumbnail_options = {
            'size': size,
            'box': box,
            'crop': True,
            'detail': True,
        }
        thumb = thumbnailer.get_thumbnail(thumbnail_options)

        return thumb.url

