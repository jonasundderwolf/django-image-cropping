from django.db import models
from django import forms
from django.conf import settings
from .widgets import ImageCropWidget, CropForeignKeyWidget


class ImageCropField(models.ImageField):
    def formfield(self, *args, **kwargs):
        kwargs['widget'] = ImageCropWidget
        return super(ImageCropField, self).formfield(*args, **kwargs)

    def south_field_triple(self):
        """
        Return a suitable description of this field for South.
        """
        # We'll just introspect ourselves, since we inherit.
        from south.modelsinspector import introspector
        field_class = "django.db.models.fields.files.ImageField"
        args, kwargs = introspector(self)
        return (field_class, args, kwargs)


class CropForeignKey(models.ForeignKey):
    '''
    A croppable image field contained in another model. Only works in admin
    for now, as it uses the raw_id widget.
    '''

    def __init__(self, model, field_name, *args, **kwargs):
        self.field_name = field_name
        super(CropForeignKey, self).__init__(model, *args, **kwargs)

    def formfield(self, *args, **kwargs):
        kwargs['widget'] = CropForeignKeyWidget(self.rel, field_name=self.field_name,
            using=kwargs.get('using'))
        return super(CropForeignKey, self).formfield(*args, **kwargs)

    def south_field_triple(self):
        """
        Return a suitable description of this field for South.
        """
        # We'll just introspect ourselves, since we inherit.
        from south.modelsinspector import introspector
        field_class = "django.db.models.fields.related.ForeignKey"
        args, kwargs = introspector(self)
        return (field_class, args, kwargs)


class ImageRatioField(models.CharField):
    def __init__(self, image_field, size, adapt_rotation=False, verbose_name=None,
                 size_warning=getattr(settings, 'IMAGE_CROPPING_SIZE_WARNING', False)):
        self.width, self.height = size.split('x')
        self.image_field = image_field
        self.adapt_rotation = adapt_rotation
        self.size_warning = size_warning
        super(ImageRatioField, self).__init__(max_length=255, blank=True, verbose_name=verbose_name)

    def formfield(self, *args, **kwargs):
        kwargs['widget'] =  forms.TextInput(attrs={
            'data-width': int(self.width),
            'data-height': int(self.height),
            'data-image-field': self.image_field,
            'data-my-name': self.name,
            'data-adapt-rotation': str(self.adapt_rotation).lower(),
            'data-size-warning': str(self.size_warning).lower(),
            'class': 'image-ratio',
        })
        return super(ImageRatioField, self).formfield(*args, **kwargs)

    def south_field_triple(self):
        """
        Return a suitable description of this field for South.
        """
        # We'll just introspect ourselves, since we inherit.
        from south.modelsinspector import introspector
        field_class = "django.db.models.fields.CharField"
        args, kwargs = introspector(self)
        return (field_class, args, kwargs)
