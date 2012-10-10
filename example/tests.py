from django.core.files import File
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase
from django.test.utils import override_settings
from django.test.client import Client
from django.test import LiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait

from example.models import Image, ImageFK

TEST_CROPPING = (355,355)

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


def create_superuser(**kwargs):
    defaults = {
        'password': 'admin',
        'username': 'admin',
        'email': 'admin@admin.test',
    }
    defaults.update(kwargs)
    return User.objects.create_superuser(**defaults)


class CroppingTestCase(TestCase):

    def test_image_cropping(self):
        """Test if the tumbnail for a cropped image gets generated with the correct box parameters."""
        image = create_cropped_image()
        c = Client()
        response = c.get(reverse('show_thumbnail', args=(image.pk,)))
        self.assertEqual(response.context['thumbnail_url'].split('.')[1], '430x360_q85_box-51%2C53%2C151%2C136_crop_detail')

    def test_image_fk_cropping(self):
        """Test if the thumbnail for CropForeignKey fields gets generated correctly."""
        image = create_cropped_image()
        example = ImageFK.objects.create(image=image, cropping=image.cropping)
        c = Client()
        response = c.get(reverse('thumbnail_foreign_key', args=(example.pk,)))
        self.assertContains(response, '120x100_q85_box-51%2C53%2C151%2C136_crop_detail')

    @override_settings(IMAGE_CROPPING_THUMB_SIZE=TEST_CROPPING)
    def test_override_image_thumb_size(self):
        """Test if the IMAGE_CROPPING_THUMB_SIZE setting is respected."""
        admin = create_superuser()
        image = create_cropped_image()
        c = Client()
        c.login(username=admin.username, password='admin')
        response = c.get(reverse('admin:example_image_change', args=[image.pk,]))
        test_url = 'data-thumbnail-url="%s.%sx%s' % (image.image_field.url, TEST_CROPPING[0], TEST_CROPPING[1])
        self.assertContains(response, test_url)


class BrowserTestCase(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        cls.selenium = WebDriver()
        super(BrowserTestCase, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(BrowserTestCase, cls).tearDownClass()

    def login(self):
        create_superuser()
        self.selenium.get('%s%s' % (self.live_server_url, '/admin'))
        username_input = self.selenium.find_element_by_id("id_username")
        password_input = self.selenium.find_element_by_id("id_password")
        username_input.send_keys('admin')
        password_input.send_keys('admin')
        self.selenium.find_element_by_xpath('//input[@value="Log in"]').click()
        WebDriverWait(self.selenium, 10)


    def test_admin_cropping(self):
        """Test if the thumbnail for cropping images gets correctly embedded in the admin."""
        image = create_cropped_image()
        self.login()
        edit_view = reverse('admin:example_image_change', args=[image.pk,])
        self.selenium.get('%s%s' % (self.live_server_url, edit_view))
        WebDriverWait(self.selenium, 10)
        thumbnail = self.selenium.find_element_by_css_selector('.jcrop-holder img')
        thumbnail_source = thumbnail.get_attribute('src')
        self.assertTrue(image.image_field.url in thumbnail_source)