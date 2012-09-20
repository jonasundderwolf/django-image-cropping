from django.contrib import admin
from image_cropping.admin import ImageCroppingMixin
from models import Image, ImageFK


class ImageFKAdmin(ImageCroppingMixin, admin.ModelAdmin):
    pass


admin.site.register(Image)
admin.site.register(ImageFK, ImageFKAdmin)
