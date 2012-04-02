from django.db import models
from image_cropping.fields import ImageRatioField, ImageCropField, CropForeignKey


class Image(models.Model):
    image_field = ImageCropField(upload_to='image/')
    cropping = ImageRatioField('image_field', '120x100')

    class Meta:
        app_label = 'example'


class ImageFK(models.Model):
    image = CropForeignKey(Image, 'image_field')
    cropping = ImageRatioField('image', '120x100')

    class Meta:
        app_label = 'example'
