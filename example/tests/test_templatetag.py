from django.test import TestCase
from django.template import Template, Context
from django.core.management import call_command

from .factory import create_cropped_image


class TemplateTagTestCase(TestCase):

    def setUp(self):
        # size of the example image is 400x400
        self.image = create_cropped_image()
        self.context = Context({'image': self.image})

    def tearDown(self):
        call_command('thumbnail_cleanup')

    def _test_templatetag(self, crop_field, options={}):
        option_str = ' '.join(['%s=%s' % (option, value)
                               for option, value in options.items()])
        tmpl = 'cropped_thumbnail image %s %s' % (crop_field, option_str)
        tmpl = '{% load cropping %}{% ' + tmpl + ' %}'
        t = Template(tmpl)
        return t.render(self.context)

    def _test_free_cropping(self, options={}):
        return self._test_templatetag('cropping_free', options)

    def _set_free_cropping(self, left, top, width, height):
        self.image.cropping_free = '%d,%d,%d,%d' % (left, top,
                                                    left + width,
                                                    top + height)
        self.image.save()

    def test_free_cropping(self):
        self._set_free_cropping(0, 0, 20, 20)
        self.assertTrue('20x20' in self._test_free_cropping())

    def test_free__max_size(self):
        self._set_free_cropping(0, 0, 20, 20)
        self._test_free_cropping()
        self.assertTrue(
            '20x20' in self._test_free_cropping({'max_size': '200x200'}))

        self._set_free_cropping(0, 0, 300, 150)
        self._test_free_cropping({'max_size': '200x200'})
        self.assertTrue(
            '200x100' in self._test_free_cropping({'max_size': '200x200'}))

        self._set_free_cropping(0, 0, 150, 300)
        self._test_free_cropping({'max_size': '200x200'})
        self.assertTrue(
            '100x200' in self._test_free_cropping({'max_size': '200x200'}))

        self._set_free_cropping(0, 0, 350, 350)
        self._test_free_cropping({'max_size': '200x200'})
        self.assertTrue(
            '200x200' in self._test_free_cropping({'max_size': '200x200'}))
