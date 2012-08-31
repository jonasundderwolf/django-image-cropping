from .widgets import ImageCropWidget, CropForeignKeyWidget


class ImageCroppingMixin(object):
    def formfield_for_dbfield(self, db_field, **kwargs):
        crop_fields = getattr(self.model, 'crop_fields', {})
        if db_field.name in crop_fields:
            target = crop_fields[db_field.name]
            if target:
                # it's a ForeignKey
                kwargs['widget'] = CropForeignKeyWidget(
                    db_field.rel,
                    field_name=crop_fields[db_field.name],
                    admin_site=self.admin_site,
                )
            else:
                # it's an ImageField
                kwargs['widget'] = ImageCropWidget

        return super(ImageCroppingMixin, self).formfield_for_dbfield(db_field, **kwargs)
