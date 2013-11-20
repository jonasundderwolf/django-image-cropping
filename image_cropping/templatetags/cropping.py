from django import template
from easy_thumbnails.files import get_thumbnailer

register = template.Library()


@register.tag
def cropped_thumbnail(parser, token):
    '''
    Syntax:
    {% cropped_thumbnail instancename ratiofieldname [scale=0.1|width=100|height=200] [upscale] %}
    '''
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
            try:  # parse option
                try:
                    option = (name, float(value))
                except ValueError:
                    if name != 'max_size':
                        raise
                    if not 'x' in value:
                        raise template.TemplateSyntaxError("%s must match INTxINT" % args[3])
                    option = (name, list(map(int, value.split('x'))))
                else:
                    if not option[0] in ('scale', 'width', 'height'):
                        raise template.TemplateSyntaxError("invalid optional argument %s" % args[3])
                    if option[1] < 0:
                        raise template.TemplateSyntaxError("%s must have a positive value" % option[0])
            except ValueError:
                raise template.TemplateSyntaxError("%s needs an numeric argument" % args[3])

        except ValueError:  # check for upscale argument
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
        image = getattr(instance, ratiofield.image_field)  # get imagefield

        if ratiofield.image_fk_field:  # image is ForeignKey
            # get the imagefield
            image = getattr(image, ratiofield.image_fk_field)
            if not image:
                return

        box = getattr(instance, self.ratiofieldname)
        if ratiofield.free_crop:
            if not box:
                size = (image.width, image.height)
            else:
                box_values = list(map(int, box.split(',')))
                size = (box_values[2] - box_values[0],
                        box_values[3] - box_values[1])
        else:
            size = (int(ratiofield.width), int(ratiofield.height))

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
            elif option[0] == 'max_size':
                max_width, max_height = option[1]
                width, height = size
                # recalculate height if needed
                if max_width < width:
                    height = height * max_width / width
                    width = max_width
                # recalculate width if needed
                if max_height < height:
                    width = max_height * width / height
                    height = max_height

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
        return thumbnailer.get_thumbnail(thumbnail_options).url
