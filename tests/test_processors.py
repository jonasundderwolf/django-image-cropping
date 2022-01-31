from PIL import ImageChops

from django.test import TestCase

from image_cropping.thumbnail_processors import crop_corners

from .factory import create_pil_image


class ProcessorTestCase(TestCase):
    def setUp(self):
        self.image = create_pil_image()

    def assertImagesEqual(self, im1, im2, msg=None):
        if im1.size != im2.size:
            raise self.failureException(
                msg or "The two images have different dimensions"
            )
        if im1.mode != im2.mode:
            msg = msg or "The two images have different modes"
            raise self.failureException("%s: %s vs. %s" % (msg, im1.mode, im2.mode))
        if ImageChops.difference(im1, im2).getbbox() is not None:
            msg = msg or "The two images were not identical"
            diff = ImageChops.difference(im1, im2).getbbox()
            raise self.failureException("%s: %s" % (msg, diff))

    def test_cropping_with_invalid_box(self):
        """Test if an invalid box is ignored and the image is simply passed through"""
        self.assertImagesEqual(self.image, crop_corners(self.image, "NaN"))

    def test_cropping_disabled(self):
        """Test disabled cropping (indicated via negative first box value)"""
        self.assertImagesEqual(self.image, crop_corners(self.image, [-1, 1, 1, 1]))

    def test_cropping_dimensions_with_box_arg_as_string(self):
        """Test if the image is cropped to the correct dimensions (box as string)"""
        cropped = crop_corners(self.image, (0, 0, 200, 200))
        self.assertTrue(cropped.size, (200, 200))

    def test_cropping_dimensions_with_box_arg_as_list(self):
        """Test if the image is cropped to the correct dimensions (box as list)"""
        cropped = crop_corners(self.image, "0, 0, 200, 200")
        self.assertTrue(cropped.size, (200, 200))
