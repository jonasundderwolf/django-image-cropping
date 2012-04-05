from .widgets import CropForeignKeyWidget


class ImageCroppingAdmin(object):

    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super(ImageCroppingAdmin, self).formfield_for_dbfield(db_field, **kwargs)

        if hasattr(db_field, 'related') and db_field.name in self.model.crop_fk_fields:
            formfield.widget = CropForeignKeyWidget(db_field.rel, field_name=db_field.field_name,
                                                    admin_site=self.admin_site)
        return formfield
