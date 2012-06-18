from django.contrib import admin
from image_cropping.admin import ImageCroppingAdmin
from models import Image, ImageFK


class ImageFKAdmin(ImageCroppingAdmin, admin.ModelAdmin):
    pass


admin.site.register(Image)
admin.site.register(ImageFK, ImageFKAdmin)
