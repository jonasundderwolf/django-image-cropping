from django.db import models
from image_cropping.fields import ImageRatioField, ImageCropField


class Image(models.Model):
    image_field = ImageCropField(upload_to='image/')
    cropping = ImageRatioField('image_field', '120x100')

    class Meta:
        app_label = 'example'


class ImageFK(models.Model):
    image = models.ForeignKey(Image)
    cropping = ImageRatioField('image__image_field', '120x100')

    class Meta:
        app_label = 'example'
