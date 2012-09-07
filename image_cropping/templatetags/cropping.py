from django import template
from easy_thumbnails.files import get_thumbnailer

register = template.Library()

# Sytanx:
# {% cropped_thumbnail instancename ratiofieldname [scale=0.1|width=100|height=200] [upscale] %}
@register.tag
def cropped_thumbnail(parser, token):
    args = token.split_contents()

    if len(args) < 3:
        # requites model and ratiofieldname
        raise template.TemplateSyntaxError("%r tag requires at least two arguments" % args[0])

    option = None
    upscale = False

    instance = args[1]
    # strip quotes from ratio field
    ratiofieldname = args[2].strip('"\'')

    # parse additional arguments
    for arg in args[3:]:
        arg = arg.lower()
        try:
            name, value = arg.split('=')

            if option:
                raise template.TemplateSyntaxError("%s: there is already an option defined!" % arg)
            try: # parse option
                option = (name, float(value))
                if not option[0] in ('scale', 'width', 'height'):
                    raise template.TemplateSyntaxError("invalid optional argument %s" % args[3])
                if option[1] < 0:
                    raise template.TemplateSyntaxError("%s must have a positive value" % option[0])
            except ValueError:
                raise template.TemplateSyntaxError("%s needs an numeric argument" % args[3])

        except ValueError: # check for upscale argument
            if arg == 'upscale':
                upscale = True
            else:
                raise template.TemplateSyntaxError("%s is an invalid option" % arg)

    return CroppingNode(instance, ratiofieldname, option, upscale)


class CroppingNode(template.Node):
    def __init__(self, instance, ratiofieldname, option=None, upscale=False):
        self.instance = instance
        self.ratiofieldname = ratiofieldname
        self.option = option
        self.upscale = upscale

    def render(self, context):
        instance = template.Variable(self.instance).resolve(context)
        if not instance:
            return

        ratiofield = instance._meta.get_field(self.ratiofieldname)
        image = getattr(instance, ratiofield.image_field) # get imagefield

        if ratiofield.image_fk_field: # image is ForeignKey
            # get the imagefield
            image = getattr(image, ratiofield.image_fk_field)

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

        if ratiofield.adapt_rotation:
            if (image.height > image.width) != (size[1] > size[0]):
                # box needs rotation
                size = (size[1], size[0])

        thumbnailer = get_thumbnailer(image)
        thumbnail_options = {
            'size': size,
            'box': box,
            'crop': True,
            'detail': True,
            'upscale': self.upscale
        }
        thumb = thumbnailer.get_thumbnail(thumbnail_options)

        return thumb.url
