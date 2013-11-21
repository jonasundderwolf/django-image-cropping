from django.core.urlresolvers import reverse
from django.core.management import call_command
from django.test import LiveServerTestCase

from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait

from .test_factory import create_superuser, create_cropped_image


class BrowserTestCase(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        cls.selenium = WebDriver()
        super(BrowserTestCase, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(BrowserTestCase, cls).tearDownClass()

    def setUp(self):
        self.image = create_cropped_image()
        self.user = create_superuser()
        super(BrowserTestCase, self).setUp()

    def tearDown(self):
        call_command('thumbnail_cleanup')
        super(BrowserTestCase, self).tearDown()

    def _ensure_page_loaded(self, url=None):
        # http://stackoverflow.com/questions/18729483/reliably-detect-page-load-or-time-out-selenium-2
        def readystate_complete(d):
            # AFAICT Selenium offers no better way to wait for the document to
            # be loaded, if one is in ignorance of its contents.
            return d.execute_script("return document.readyState") == "complete"

        try:
            if url:
                self.selenium.get(url)
            # maximum wait: 30s
            WebDriverWait(self.selenium, 30).until(readystate_complete)
        except TimeoutException:
            self.selenium.execute_script("window.stop();")

    def _login(self):
        self._ensure_page_loaded('%s%s' % (self.live_server_url, '/admin'))
        username_input = self.selenium.find_element_by_id("id_username")
        password_input = self.selenium.find_element_by_id("id_password")
        username_input.send_keys('admin')
        password_input.send_keys('admin')
        self.selenium.find_element_by_xpath('//input[@value="Log in"]').click()
        self._ensure_page_loaded()

    def _load_image_admin(self):
        self._login()

        edit_view = reverse('admin:example_image_change', args=[self.image.pk])
        self._ensure_page_loaded('%s%s' % (self.live_server_url, edit_view))

    def test_admin__widget_rendered(self):
        self._load_image_admin()
        widget = self.selenium.find_element_by_css_selector('.field-cropping '
                                                            '.image-ratio')

        self.assertEqual(int(widget.get_attribute('data-width')), 120)
        self.assertEqual(int(widget.get_attribute('data-height')), 100)
        self.assertEqual(widget.get_attribute('data-image-field'),
                         'image_field')
        self.assertEqual(widget.get_attribute('data-my-name'), 'cropping')
        self.assertEqual(widget.get_attribute('data-allow-fullsize'), 'true')
        self.assertEqual(widget.get_attribute('data-size-warning'), 'false')
        self.assertEqual(widget.get_attribute('data-adapt-rotation'), 'false')
        # TODO this differs by one pixel
        #self.assertEqual(widget.get_attribute('value'), self.image.cropping)

    def test_admin__ensure_thumbnail_available(self):
        self._load_image_admin()
        img = self.selenium.find_element_by_css_selector('.field-cropping img')
        self.assertTrue(self.image.image_field.url in img.get_attribute('src'))

    def test_admin__ensure_jcrop_initialized(self):
        self._load_image_admin()
        WebDriverWait(self.selenium, 10)  # so jcrop gets loaded
        try:
            self.selenium.find_element_by_css_selector('.field-cropping '
                                                       '.jcrop-holder')
        except NoSuchElementException:
            self.fail('JCrop not initialized')


    # TODO
    #  - data-attributes are correct (false, true, ...)
    #  - test cropping
    #  - test ratio is preserved
    #  - test size warning
    #  - test allow_fullsize
    #  - test modelform

    """
    def test_modelform_cropping(self):
        ""Test if the thumbnail for cropping images gets correctly embedded when using modelforms.""
        image = create_cropped_image()
        edit_view = reverse('modelform_example', args=[image.pk])
        self.selenium.get('%s%s' % (self.live_server_url, edit_view))
        WebDriverWait(self.selenium, 10)
        thumbnail = self.selenium.find_element_by_css_selector('.jcrop-holder img')
        thumbnail_source = thumbnail.get_attribute('src')
        self.assertTrue(image.image_field.url in thumbnail_source)
    """
