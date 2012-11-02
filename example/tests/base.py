from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.utils import override_settings

from example.models import ImageFK
from .factory import create_cropped_image, create_superuser

TEST_CROPPING = (355,355)

class CroppingTestCase(TestCase):

    def test_image_cropping(self):
        """Test if the tumbnail for a cropped image gets generated with the correct box parameters."""
        image = create_cropped_image()
        response = self.client.get(reverse('show_thumbnail', args=(image.pk,)))
        self.assertEqual(response.context['thumbnail_url'].split('.')[1], '430x360_q85_box-51%2C53%2C151%2C136_crop_detail')

    def test_image_fk_cropping(self):
        """Test if the thumbnail for CropForeignKey fields gets generated correctly."""
        image = create_cropped_image()
        example = ImageFK.objects.create(image=image, cropping=image.cropping)
        response = self.client.get(reverse('thumbnail_foreign_key', args=(example.pk,)))
        self.assertContains(response, '120x100_q85_box-51%2C53%2C151%2C136_crop_detail')

    @override_settings(IMAGE_CROPPING_THUMB_SIZE=TEST_CROPPING)
    def test_override_image_thumb_size(self):
        """Test if the IMAGE_CROPPING_THUMB_SIZE setting is respected."""
        admin = create_superuser()
        image = create_cropped_image()
        self.client.login(username=admin.username, password='admin')
        response = self.client.get(reverse('admin:example_image_change', args=[image.pk,]))
        test_url = 'data-thumbnail-url="%s.%sx%s' % (image.image_field.url, TEST_CROPPING[0], TEST_CROPPING[1])
        self.assertContains(response, test_url)
