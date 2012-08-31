import warnings
from django.db import models
from django import forms
from django.conf import settings
from .widgets import ImageCropWidget


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


#deprecated, as we now set the widget in the ModelAdmin
class CropForeignKey(models.ForeignKey):
    '''
    A croppable image field contained in another model. Only works in admin
    for now, as it uses the raw_id widget.
    '''

    def __init__(self, model, field_name, *args, **kwargs):
        self.field_name = field_name
        warnings.warn('Please use the ImageCroppingMixin in your ModelAdmin '
                      'instead of a CropForeignKey!', DeprecationWarning)
        super(CropForeignKey, self).__init__(model, *args, **kwargs)

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
    def __init__(self, image_field, size, adapt_rotation=False, allow_fullsize=False, verbose_name=None, help_text=None,
                 size_warning=getattr(settings, 'IMAGE_CROPPING_SIZE_WARNING', False)):
        if '__' in image_field:
            self.image_field, self.image_fk_field = image_field.split('__')
        else:
            self.image_field, self.image_fk_field = image_field, None
        self.width, self.height = size.split('x')
        self.adapt_rotation = adapt_rotation
        self.allow_fullsize = allow_fullsize
        self.size_warning = size_warning
        super(ImageRatioField, self).__init__(max_length=255, blank=True, verbose_name=verbose_name, help_text=help_text)

    def contribute_to_class(self, cls, name):
        super(ImageRatioField, self).contribute_to_class(cls, name)
        # attach a list of fields that are referenced by the ImageRatioField
        # so we can set the correct widget in the ModelAdmin
        if not hasattr(cls, 'crop_fields'):
            cls.add_to_class('crop_fields', {})
        cls.crop_fields[self.image_field] = self.image_fk_field

    def formfield(self, *args, **kwargs):
        kwargs['widget'] = forms.TextInput(attrs={
            'data-width': int(self.width),
            'data-height': int(self.height),
            'data-image-field': self.image_field,
            'data-my-name': self.name,
            'data-adapt-rotation': str(self.adapt_rotation).lower(),
            'data-allow-fullsize': str(self.allow_fullsize).lower(),
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
