from __future__ import unicode_literals
from . import widgets


class ImageCroppingMixin(object):
    def formfield_for_dbfield(self, db_field, **kwargs):
        crop_fields = getattr(self.model, 'crop_fields', {})
        if db_field.name in crop_fields:
            target = crop_fields[db_field.name]
            if target['fk_field']:
                # it's a ForeignKey
                kwargs['widget'] = widgets.CropForeignKeyWidget(
                    db_field.rel,
                    field_name=target['fk_field'],
                    admin_site=self.admin_site,
                )
            elif target['hidden']:
                # it's a hidden ImageField
                kwargs['widget'] = widgets.HiddenImageCropWidget
            else:
                # it's a regular ImageField
                kwargs['widget'] = widgets.ImageCropWidget

        return super(ImageCroppingMixin, self).formfield_for_dbfield(db_field, **kwargs)
