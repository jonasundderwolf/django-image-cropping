import os

from example.models import Image, ImageFK

from django.conf import settings
from django.core.files import File
from django.test import TestCase

from image_cropping.utils import max_cropping


class InitialCroppingTestCase(TestCase):
    def setUp(self):
        self.path = "%s%s" % (settings.STATIC_ROOT, "/images/example_image.jpg")
        self.width = 400
        self.height = 400

        self.image = Image()
        self.image.image_field.save(
            os.path.basename(self.path), File(open(self.path, "rb"))
        )
        self.image.save()

    def test_maxcropping(self):
        # normal crop
        self.assertEqual([0, 0, 400, 400], max_cropping(100, 100, 400, 400))
        self.assertEqual([100, 0, 300, 400], max_cropping(100, 200, 400, 400))
        self.assertEqual([0, 100, 400, 300], max_cropping(200, 100, 400, 400))

        # free crop
        self.assertEqual([0, 0, 400, 400], max_cropping(100, 100, 400, 400, True))
        self.assertEqual([0, 0, 400, 400], max_cropping(100, 200, 400, 400, True))
        self.assertEqual([0, 0, 400, 400], max_cropping(200, 100, 400, 400, True))

        # to small
        self.assertEqual([0, 0, 100, 100], max_cropping(200, 200, 100, 100))
        self.assertEqual([0, 25, 100, 75], max_cropping(200, 100, 100, 100))
        self.assertEqual([25, 0, 75, 100], max_cropping(100, 200, 100, 100))

    def test_initialcropping(self):
        self.assertEqual(
            self.image.cropping,
            ",".join(
                map(lambda d: str(d), max_cropping(120, 100, self.width, self.height))
            ),
        )

        # free crop
        self.assertEqual(
            self.image.cropping_free,
            ",".join(
                map(
                    lambda d: str(d),
                    max_cropping(120, 100, self.width, self.height, True),
                )
            ),
        )

    def test_fk_initialcropping(self):
        image = ImageFK(image=self.image)
        image.save()
        self.assertEqual(
            image.cropping,
            ",".join(
                map(lambda d: str(d), max_cropping(120, 100, self.width, self.height))
            ),
        )
