from pyvirtualdisplay import Display
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait

from django.core.urlresolvers import reverse
from django.test.utils import override_settings

from image_cropping.config import settings

from . import factory

try:
    from django.contrib.staticfiles.testing import (
        StaticLiveServerTestCase as LiveServerTestCase)
except ImportError:
    from django.test import LiveServerTestCase


class BrowserTestBase(object):

    @classmethod
    def setUpClass(cls):
        if settings.HEADLESS:
            cls.display = Display(visible=0, size=(1024, 768))
            cls.display.start()
        cls.selenium = WebDriver()
        super(BrowserTestBase, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        if settings.HEADLESS:
            cls.display.stop()
        super(BrowserTestBase, cls).tearDownClass()

    def setUp(self):
        self.image = factory.create_cropped_image()
        self.user = factory.create_superuser()
        super(BrowserTestBase, self).setUp()

    def _ensure_page_loaded(self, url=None):
        # see: http://stackoverflow.com/questions/18729483/
        #             reliably-detect-page-load-or-time-out-selenium-2
        def readystate_complete(d):
            return d.execute_script("return document.readyState") == "complete"

        try:
            if url:
                self.selenium.get(url)
            WebDriverWait(self.selenium, 45).until(readystate_complete)
        except TimeoutException:
            self.selenium.execute_script("window.stop();")

    def _ensure_widget_rendered(self, **options):
        defaults = {
            'data-min-width': '120',
            'data-min-height': '100',
            'data-image-field': 'image_field',
            'data-my-name': 'cropping',
            'data-allow-fullsize': 'true',
            'data-size-warning': 'false',
            'data-adapt-rotation': 'false'
        }
        defaults.update(options)
        widget = self.selenium.find_element_by_css_selector('.image-ratio')
        for attr in defaults.keys():
            self.assertEqual(widget.get_attribute(attr), defaults[attr])

    def _ensure_thumbnail_rendered(self):
        img = self.selenium.find_element_by_css_selector('.image-ratio + img')
        self.assertTrue(self.image.image_field.url in img.get_attribute('src'))

    def _ensure_jcrop_initialized(self):
        # make sure Jcrop is properly loaded
        def jcrop_initialized(d):
            try:
                d.find_element_by_css_selector('.jcrop-holder')
            except NoSuchElementException:
                return False
            return True

        try:
            WebDriverWait(self.selenium, 45).until(jcrop_initialized)
        except TimeoutException:
            self.selenium.execute_script("window.stop();")
            self.fail('Jcrop not initialized')


class AdminImageCroppingTestCase(BrowserTestBase, LiveServerTestCase):
    def setUp(self):
        super(AdminImageCroppingTestCase, self).setUp()
        self._ensure_page_loaded('%s%s' % (self.live_server_url, '/admin'))
        username_input = self.selenium.find_element_by_id("id_username")
        password_input = self.selenium.find_element_by_id("id_password")
        username_input.send_keys(factory.TEST_USERNAME)
        password_input.send_keys(factory.TEST_PASSWORD)
        self.selenium.find_element_by_xpath('//input[@value="Log in"]').click()
        self._ensure_page_loaded()

    def test_widget_rendered(self):
        edit_view = reverse('admin:example_image_change', args=[self.image.pk])
        self._ensure_page_loaded('%s%s' % (self.live_server_url, edit_view))
        self._ensure_widget_rendered()
        self._ensure_thumbnail_rendered()


class ModelFormCroppingTestCase(BrowserTestBase, LiveServerTestCase):

    def test_widget_rendered(self):
        edit_view = reverse('modelform_example', args=[self.image.pk])
        self._ensure_page_loaded('%s%s' % (self.live_server_url, edit_view))
        self._ensure_widget_rendered()
        self._ensure_thumbnail_rendered()


class CropForeignKeyTest(AdminImageCroppingTestCase):

    def test_fk_cropping(self):
        changelist_view = reverse('admin:example_imagefk_changelist')
        self._ensure_page_loaded('%s%s' % (self.live_server_url, changelist_view))
        self.selenium.find_element_by_css_selector('.addlink').click()
        self.selenium.find_element_by_css_selector('#lookup_id_image').click()
        self.selenium.switch_to_window(self.selenium.window_handles[1])
        self.selenium.find_element_by_css_selector('#result_list a').click()
        self.selenium.switch_to_window(self.selenium.window_handles[0])
        self.selenium.find_element_by_xpath(
            '//input[@value="Save and continue editing"]').click()
        self._ensure_jcrop_initialized()
        self.selenium.find_element_by_css_selector('.jcrop-holder')
        self._ensure_widget_rendered(**{
            'data-allow-fullsize': 'false',
            'data-image-field': 'image'}
        )
        self._ensure_thumbnail_rendered()

    def test_fk_cropping_with_non_existent_fk_target(self):
        """Test if referencing a non existing image as fk target is not allowed"""
        changelist_view = reverse('admin:example_imagefk_changelist')
        self._ensure_page_loaded('%s%s' % (self.live_server_url, changelist_view))
        self.selenium.find_element_by_css_selector('.addlink').click()
        image_input = self.selenium.find_element_by_id("id_image")
        image_input.send_keys('10')
        self.selenium.find_element_by_xpath(
            '//input[@value="Save and continue editing"]').click()
        self._ensure_page_loaded()
        self.selenium.find_element_by_css_selector('.form-row.errors.field-image')


class SettingsTest(AdminImageCroppingTestCase):

    def test_widget_width_default(self):
        edit_view = reverse('admin:example_image_change', args=[self.image.pk])
        self._ensure_page_loaded('%s%s' % (self.live_server_url, edit_view))
        img = self.selenium.find_element_by_css_selector('.image-ratio + img')
        self.assertEqual(
            int(img.get_attribute('width')), settings.IMAGE_CROPPING_THUMB_SIZE[0])

    @override_settings(IMAGE_CROPPING_THUMB_SIZE=(500, 500))
    def test_widget_width_overridden(self):
        edit_view = reverse('admin:example_image_change', args=[self.image.pk])
        self._ensure_page_loaded('%s%s' % (self.live_server_url, edit_view))
        img = self.selenium.find_element_by_css_selector('.image-ratio + img')
        self.assertEqual(int(img.get_attribute('width')), 500)
