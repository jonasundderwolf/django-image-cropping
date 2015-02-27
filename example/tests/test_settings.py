from django_webtest import WebTest
from django.core.urlresolvers import reverse
from django.test.utils import override_settings
from . import factory


class AdminTestCase(WebTest):

    def setUp(self):
        super(AdminTestCase, self).setUp()
        self.user = factory.create_superuser()
        self.image = factory.create_cropped_image()

    def test_jquery_included(self):
        edit_view = reverse('admin:example_image_change', args=[self.image.pk])
        response = self.app.get(edit_view, user=self.user)
        self.assertTrue('src="/static/js/jquery.min.js">' in response.content)

    @override_settings(IMAGE_CROPPING_JQUERY_URL=None)
    def test_jquery_not_included(self):
        edit_view = reverse('admin:example_image_change', args=[self.image.pk])
        response = self.app.get(edit_view, user=self.user)
        self.assertFalse('src="/static/js/jquery.min.js">' in response.content)
