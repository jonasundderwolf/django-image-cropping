import itertools

from django.test import TestCase
from django.template import Template, Context
from django.core.management import call_command

from .factory import create_cropped_image


class TemplateTagTestBase(object):
    def setUp(self):
        # size of the example image is 400x400
        # cropping size is 120x100
        self.image = create_cropped_image()
        self.context = Context({'image': self.image})

    def tearDown(self):
        try:
            call_command('thumbnail_cleanup')
        except IndexError:
            pass

    def _test_templatetag(self, crop_field, options={}):
        option_str = ' '.join(['%s=%s' % (option, value)
                               for option, value in options.items()])
        tmpl = 'cropped_thumbnail image "%s" %s' % (crop_field, option_str)
        tmpl = '{% load cropping %}{% ' + tmpl + ' %}'
        t = Template(tmpl)
        return t.render(self.context)


class CroppingTestCase(TemplateTagTestBase, TestCase):
    def assertRaisesWithMessage(self, msg, func, *args, **kwargs):
        # http://stackoverflow.com/a/8673096
        try:
            func(*args, **kwargs)
            self.assertFail()
        except Exception as e:
            self.assertEqual(e.args[0], msg)

    def _test_cropping(self, options={}):
        return self._test_templatetag('cropping', options)

    def test_cropping(self):
        self.assertTrue('120x100' in self._test_cropping())

    def test_only_one_size_modifier_allowed(self):
        def powerset(iterable):
            s = list(iterable)
            return itertools.chain.from_iterable(itertools.combinations(s, r)
                                                 for r in range(2, len(s)+1))

        valid_options = (('scale', 0.5), ('width', 100),
                         ('height', 100), ('max_size', '100x200'))

        for kwargs in powerset(valid_options):
            self.assertRaisesWithMessage(
                'Only one size modifier is allowed.',
                self._test_cropping, dict(kwargs))

    def test_scale(self):
        self.assertTrue('60x50' in self._test_cropping({'scale': 0.5}))

    def test_width(self):
        self.assertTrue('240x200' in self._test_cropping({'width': 240}))

    def test_height(self):
        self.assertTrue('240x200' in self._test_cropping({'height': 200}))

    def test_max_size_value(self):
        self.assertRaisesWithMessage(
            'max_size must match INTxINT',
            self._test_cropping, {'max_size': 200})
        self.assertRaisesWithMessage(
            'max_size must match INTxINT',
            self._test_cropping, {'max_size': '200i100'})
        self.assertRaisesWithMessage(
            'max_size must match INTxINT',
            self._test_cropping, {'max_size': '200i'})
        self.assertRaisesWithMessage(
            'max_size must match INTxINT',
            self._test_cropping, {'max_size': '"200"'})
        self.assertRaisesWithMessage(
            'max_size must match INTxINT',
            self._test_cropping, {'max_size': '"200i100"'})
        self.assertRaisesWithMessage(
            'max_size must match INTxINT',
            self._test_cropping, {'max_size': '"200i"'})

    def test_max_size(self):  # 120x100
        self.assertTrue(
            '120x100' in self._test_cropping({'max_size': '"200x200"'}))
        self.assertTrue(
            '60x50' in self._test_cropping({'max_size': '"120x50"'}))
        self.assertTrue(
            '60x50' in self._test_cropping({'max_size': '"60x100"'}))
        self.assertTrue(
            '60x50' in self._test_cropping({'max_size': '"60x50"'}))

    def test_upscale(self):
        # no upscale Test
        # upscale test
        pass

    def test_adapt_rotation(self):
        pass


class FreeCroppingTestCase(TemplateTagTestBase, TestCase):
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
        self.assertTrue(
            '20x20' in self._test_free_cropping({'max_size': '"200x200"'}))

        self._set_free_cropping(0, 0, 300, 150)
        self.assertTrue(
            '200x100' in self._test_free_cropping({'max_size': '"200x200"'}))

        self._set_free_cropping(0, 0, 150, 300)
        self.assertTrue(
            '100x200' in self._test_free_cropping({'max_size': '"200x200"'}))

        self._set_free_cropping(0, 0, 350, 350)
        self.assertTrue(
            '200x200' in self._test_free_cropping({'max_size': '"200x200"'}))
