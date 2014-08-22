from django.core.urlresolvers import reverse
from django.test import LiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from .test_factory import create_superuser, create_cropped_image


class BrowserTestCase(LiveServerTestCase):

    def setUp(self):
        self.browser = WebDriver()

        super(BrowserTestCase, self).setUp()

    def tearDown(self):
        self.browser.quit()
        super(BrowserTestCase, self).tearDown()

    def login(self):
        create_superuser()
        self.browser.get('%s%s' % (self.live_server_url, '/admin'))
        username_input = self.browser.find_element_by_id("id_username")
        password_input = self.browser.find_element_by_id("id_password")
        username_input.send_keys('admin')
        password_input.send_keys('admin')
        self.browser.find_element_by_xpath('//input[@value="Log in"]').click()

    def test_admin_cropping(self):
        """Test if the thumb for cropping images gets embedded in the admin."""
        image = create_cropped_image()
        self.login()
        edit_view = reverse('admin:example_image_change', args=[image.pk])
        self.browser.get('%s%s' % (self.live_server_url, edit_view))
        WebDriverWait(self.browser, 10)
        thumbnail = self.browser.find_elements_by_xpath(
            "//*[contains(concat(' ', normalize-space(@class), ' '), ' jcrop-holder ')]/img")[0]
        thumbnail_source = thumbnail.get_attribute('src')
        self.assertTrue(image.image_field.url in thumbnail_source)

    def test_modelform_cropping(self):
        """Test if the thumb for cropping images gets embedded when using ModelForms."""
        image = create_cropped_image()
        edit_view = reverse('modelform_example', args=[image.pk])
        self.browser.get('%s%s' % (self.live_server_url, edit_view))
        WebDriverWait(self.browser, 10)
        thumbnail = self.browser.find_elements_by_xpath(
            "//*[contains(concat(' ', normalize-space(@class), ' '), ' jcrop-holder ')]/img")[0]
        thumbnail_source = thumbnail.get_attribute('src')
        self.assertTrue(image.image_field.url in thumbnail_source)
