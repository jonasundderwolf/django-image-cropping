from django.contrib import admin
from .widgets import CropForeignKeyWidget
from .fields import CropForeignKey

class ImageCroppingAdmin(admin.ModelAdmin):

    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super(ImageCroppingAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if isinstance(db_field, CropForeignKey):
            formfield.widget = CropForeignKeyWidget(db_field.rel, field_name=db_field.name, using=kwargs.get('using'))
            #Django 1.4: pass a reference to the admin_site which is nowadays needed by ForeignKeyRawIdWidget
            #formfield.widget = CropForeignKeyWidget(db_field.rel, field_name=db_field.name, using=kwargs.get('using'), admin_site=self.admin_site)
        return formfield
