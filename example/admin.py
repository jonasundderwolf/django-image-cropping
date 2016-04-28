from django.contrib import admin

from image_cropping.admin import ImageCroppingMixin

from .models import Image, ImageFK


class ImageFKAdmin(ImageCroppingMixin, admin.ModelAdmin):
    pass


class ImageAdmin(ImageCroppingMixin, admin.ModelAdmin):
    pass


admin.site.register(Image, ImageAdmin)
admin.site.register(ImageFK, ImageFKAdmin)
