from django.core.files import File
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client
from django.conf import settings
from example.models import Image


def create_cropped_image(**kwargs):
    defaults = {
        'image_cropping':  u'51,53,151,136',
        'image_path': settings.STATIC_ROOT + "/images/example_image.jpg",
        'image_name': 'example_image',
    }
    defaults.update(kwargs)
    image = Image.objects.create(**{'cropping': defaults['image_cropping']})
    image.image_field.save(defaults['image_name'], File(open(defaults['image_path'])), True)
    return image


class CroppingTestCase(TestCase):

    def test_cropping(self):
        """Test if the tumbnail for a cropped image gets generated with the correct box parameters."""
        image = create_cropped_image()
        c = Client()
        response = c.get(reverse('show_thumbnail', args=(image.pk,)))
        self.assertEqual(response.context['thumbnail_url'].split('.')[1], '430x360_q85_box-51%2C53%2C151%2C136_crop_detail')
