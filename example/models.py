from django.db import models

from image_cropping.fields import ImageCropField, ImageRatioField


class Image(models.Model):
    image_field = ImageCropField(upload_to="image/")
    cropping = ImageRatioField("image_field", "120x100", allow_fullsize=True)
    cropping_free = ImageRatioField(
        "image_field", "300x230", free_crop=True, size_warning=True
    )

    class Meta:
        app_label = "example"

    def get_cropping_as_list(self):
        if self.cropping:
            return list(map(int, self.cropping.split(",")))


class ImageFK(models.Model):
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    cropping = ImageRatioField("image__image_field", "120x100")

    class Meta:
        app_label = "example"
