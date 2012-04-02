from django import VERSION
from .widgets import CropForeignKeyWidget


class ImageCroppingAdmin(object):

    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super(ImageCroppingAdmin, self).formfield_for_dbfield(db_field, **kwargs)

        if hasattr(db_field, 'related') and db_field.name in self.model.crop_fk_fields:
            #Django 1.4: pass a reference to the admin_site which is nowadays needed by ForeignKeyRawIdWidget
            kwargs = {'admin_site': self.admin_site} if VERSION >= (1, 4, 0) else {}
            formfield.widget = CropForeignKeyWidget(db_field.rel, field_name=db_field.name, **kwargs)
        return formfield
