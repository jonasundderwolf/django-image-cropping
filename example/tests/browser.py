from django.core.urlresolvers import reverse
from django.test import LiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from .factory import create_superuser, create_cropped_image

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

    def test_modelform_cropping(self):
        """Test if the thumbnail for cropping images gets correctly embedded when using modelforms."""
        image = create_cropped_image()
        edit_view = reverse('modelform_example', args=[image.pk,])
        self.selenium.get('%s%s' % (self.live_server_url, edit_view))
        WebDriverWait(self.selenium, 10)
        thumbnail = self.selenium.find_element_by_css_selector('.jcrop-holder img')
        thumbnail_source = thumbnail.get_attribute('src')
        self.assertTrue(image.image_field.url in thumbnail_source)
