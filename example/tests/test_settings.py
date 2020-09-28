from django_webtest import WebTest

from django.test.utils import override_settings
from django.urls import reverse

from . import factory


class SettingsTestCase(WebTest):
    def setUp(self):
        super().setUp()
        self.user = factory.create_superuser()
        self.image = factory.create_cropped_image()

    def test_jquery_included(self):
        edit_view = reverse("admin:example_image_change", args=[self.image.pk])
        response = self.app.get(edit_view, user=self.user)
        self.assertContains(response, 'src="/static/js/jquery.min.js"')

    @override_settings(IMAGE_CROPPING_JQUERY_URL=None)
    def test_jquery_not_included(self):
        edit_view = reverse("admin:example_image_change", args=[self.image.pk])
        response = self.app.get(edit_view, user=self.user)
        self.assertNotContains(response, 'src="/static/js/jquery.min.js"')
