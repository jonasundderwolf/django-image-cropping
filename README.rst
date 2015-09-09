=====================
django-image-cropping
=====================

.. image:: https://pypip.in/v/django-image-cropping/badge.png
    :target: https://pypi.python.org/pypi/django-image-cropping

.. image:: https://travis-ci.org/jonasundderwolf/django-image-cropping.png?branch=master
    :target: http://travis-ci.org/jonasundderwolf/django-image-cropping
    :alt: Build Status

.. image:: https://coveralls.io/repos/jonasundderwolf/django-image-cropping/badge.png?branch=master
    :target: https://coveralls.io/r/jonasundderwolf/django-image-cropping
    :alt: Coverage

django-image-cropping is an app for cropping uploaded images via Django's admin backend using `Jcrop
<https://github.com/tapmodo/Jcrop>`_.

Screenshot:

.. image:: http://www.jonasundderwolf.de/media/images/django_image_cropping_example.png

django-image-cropping is perfect when you need images with a specific size for your templates but want your
users or editors to upload images of any dimension. It presents a selection with a fixed aspect ratio so your users
can't break the layout with oddly-sized images.

The original images are kept intact and only get cropped when they are displayed.
Large images are presented in a small format, so even very big images can easily be cropped.

The necessary fields, widgets and a template tag for displaying the
cropped image in your templates are provided.

Also works with `FeinCMS <https://github.com/feincms/feincms>`_ content types!

Installation
============

#. Install django-image-cropping using ``pip``::

    pip install django-image-cropping

#. If you haven't installed easy_thumbnails already, install it::

    pip install easy_thumbnails

#. Add ``easy_thumbnails`` and ``image_cropping`` to your ``INSTALLED_APPS``.

#. Adjust the thumbnail processors for ``easy-thumbnails`` in your ``settings``::

    from easy_thumbnails.conf import Settings as thumbnail_settings
    THUMBNAIL_PROCESSORS = (
        'image_cropping.thumbnail_processors.crop_corners',
    ) + thumbnail_settings.THUMBNAIL_PROCESSORS

Configuration
=============

Add an ``ImageRatioField`` to the model that contains the ``ImageField`` for the images you want to crop.

The ``ImageRatioField`` simply stores the boundaries of the cropped image.
It expects the name of the associated ``ImageField`` and the desired size of the cropped image as arguments.

The size is passed in as a string and defines the aspect ratio of the selection *as well* as the minimum
size for the final image::

    from django.db import models
    from image_cropping import ImageRatioField

    class MyModel(models.Model):
        image = models.ImageField(blank=True, upload_to='uploaded_images')
        # size is "width x height"
        cropping = ImageRatioField('image', '430x360')

You can configure a `size warning`_ if users try to crop a selection smaller than the defined minimum.

Admin Integration
=================

Add the ``ImageCroppingMixin`` to your ``ModelAdmin``::

    from django.contrib import admin
    from image_cropping import ImageCroppingMixin

    class MyModelAdmin(ImageCroppingMixin, admin.ModelAdmin):
        pass

    admin.site.register(MyModel, MyModelAdmin)

If your setup is correct you should now see the enhanced image widget that provides a selection
area.

Frontend
========

django-image-cropping provides a templatetag for displaying a cropped thumbnail.
Any other processor parameter (like ``bw=True`` or ``upscale=True``) will be forwarded to ``easy-thumbnails``::

    {% cropped_thumbnail yourmodelinstance "ratiofieldname" [scale=INT|width=INT|height=INT|max_size="INTxINT"] %}

Example usage::

    {% load cropping %}
    <img src="{% cropped_thumbnail yourmodel "cropping" scale=0.5 %}">

You can also use the standard ``easy-thumbnails`` templatetag with the ``box`` parameter::

    {% load thumbnail %}
    {% thumbnail yourmodel.image 430x360 box=yourmodel.cropping crop detail %}

Or generate the URL from Python code in your view::

    from easy_thumbnails.files import get_thumbnailer
    thumbnail_url = get_thumbnailer(yourmodel.image).get_thumbnail({
        'size': (430, 360),
        'box': yourmodel.cropping,
        'crop': True,
        'detail': True,
    }).url


ModelForm
=========

If you want to use the cropping widget outside the admin, you'll need to define the ``ImageField`` as
an ``ImageCropField``::

    from django.db import models
    from image_cropping import ImageCropField, ImageRatioField

    class MyModel(models.Model):
        image = ImageCropField(blank=True, upload_to='uploaded_images')
        # size is "width x height"
        cropping = ImageRatioField('image', '430x360')


Alternatively, override the widget in your ModelForm (you just need to do one of these two, not both!)::

    from django import forms
    from image_cropping import ImageCropWidget

    class MyModelForm(forms.ModelForm):
        class Meta:
            widgets = {
                'image': ImageCropWidget,
            }


Remember to include the form media in the ``<head>`` of your HTML::

    <html>
      <head>
        {{ form.media }}
      </head>
      <body>
        {{ form }}
      </body>
    </html>

The cropping itself happens in the ``ImageRatioField``, the ``ImageCropField`` will still behave like a regular ``ImageField``.

If you're selectively including or excluding fields from the ModelForm, remember to include the ``ImageRatioField``.


Multiple formats
================

If you need the same image in multiple formats, simply specify another ``ImageRatioField``.
This will allow the image to be cropped twice::

    from image_cropping import ImageRatioField, ImageCropField

    image = ImageCropField(blank=True, upload_to='uploaded_images')
    # size is "width x height"
    list_page_cropping = ImageRatioField('image', '200x100')
    detail_page_cropping = ImageRatioField('image', '430x360')

In your templates, use the corresponding ratio field::

    {% load cropping %}
    {% cropped_thumbnail yourmodel "list_page_cropping" %}


Foreign Keys
============

If you need to crop an image contained within another model, referenced by a ForeignKey, the ``ImageRatioField`` is
composed of the ``ForeignKey`` name, a double underscore, and the ``ImageField`` name::

    from django.db import models
    from image_cropping.fields import ImageRatioField

    class Image(models.Model):
        image_field = models.ImageField(upload_to='image/')

    class NewsItem(models.Model):
        title = models.CharField(max_length=255)
        image = models.ForeignKey(Image)
        cropping = ImageRatioField('image__image_field', '120x100')

Cropping foreign keys only works in the admin for now, as it reuses the ``raw_id`` widget.


.. _free cropping:

Free cropping
=============

If you do not need a *fixed* ratio, you can disable this constraint by setting ``free_crop`` to ``True``.
In this case the size parameter is the desired minimum and is also used for the size-warning::

    from image_cropping import ImageRatioField, ImageCropField

    image = ImageCropField(blank=True, upload_to='uploaded_images')

    # size is "width x height" so a minimum size of 200px x 100px would look like this:
    min_free_cropping = ImageRatioField('image', '200x100', free_crop=True)

Use the ``max_size`` parameter of the templatetag if you want to limit the display size of a thumbnail::

     <img src="{% cropped_thumbnail image "cropping_free" max_size="200x200" %}" />


Disabling cropping
==================

If you want cropping to be optional, use ``allow_fullsize=True`` as an additional keyword argument for your ``ImageRatioField``.

Editors can now switch off cropping by unchecking a checkbox next to the image cropping widget::

     image_with_optional_cropping = ImageRatioField('image', '200x100', allow_fullsize=True)


Settings
========

Thumbnail size
--------------

You can define the maximum size of the admin preview thumbnail in your ``settings``::

    # size is "width x height"
    IMAGE_CROPPING_THUMB_SIZE = (300, 300)

.. _size warning:

Size warning
------------

You can warn users about crop selections that are smaller than the size defined in the ``ImageRatioField``.
When users try to do a smaller selection, a red border appears around the image.

To use this functionality for a single image add the ``size_warning`` parameter to the ``ImageRatioField``::

    cropping = ImageRatioField('image', '430x360', size_warning=True)

You can enable this functionality project-wide by adding the following line to your ``settings``::

    IMAGE_CROPPING_SIZE_WARNING = True


Custom jQuery
-------------

By default the image cropping widget embeds a recent version of jQuery.

You can point to another version using the ``IMAGE_CROPPING_JQUERY_URL`` setting, though compatibility
issues may arise if your jQuery version differs from the one that is tested against.

You can also set ``IMAGE_CROPPING_JQUERY_URL`` to ``None`` to disable inclusion of jQuery by the widget.
You are now responsible for including ``jQuery`` yourself, both in the frontend and in the admin interface.


Troubleshooting
===============

The cropping widget is not displayed when using a ``ForeignKey``.
    Make sure you do **not** add the corresponding image field to ``raw_id_fields``.


Changelog
=========

1.0
---

"If your software is being used in production, it should probably already be 1.0.0." (http://semver.org)

0.9
---

This release addresses mainly the test coverage and internal stuff.

Noteable (breaking) changes and things to be considered when upgrading from an older version:

- `django-appconf <https://github.com/jezdez/django-appconf>`_ is now used for handling defaults and settings.

  * **Breaking Change**: JQUERY_URL changed to IMAGE_CROPPING_JQUERY_URL as part of this transition.

- The ``cropped_thumbnail`` tag is now based on Django's ``simple tag``.

  * **Breaking Change**: Arguments for the the tag now need to be put in quotes.
  * If you are still using Django 1.4 remember that `you can't easily use <http://stackoverflow.com/q/11804315/630877>`_ ``True`` or ``False`` as template tag arguments.

- Any processor parameter (like bw=True or upscale=True) can be used in the ``cropped_thumbnail`` tag.

- Moved inline css to a dedicated ``image_cropping.css`` style sheet

0.8
---

- **Minimum** requirements changed to **Django 1.4** and **easy-thumbnails 1.4**
- Added Python 3 compatibility. Python 2.6 is now the minimum required Python version.
- Added a `free cropping`_ option, so cropping is no longer restricted to fixed ratios.
- Removed the deprecated ``CropForeignKey`` field.

0.7
---

- Made the widget for the ``ImageCropField`` overwriteable to allow custom widgets. (Remember to use the ``ImageCroppingMixin`` in the admin as the image cropping widgets are no longer implicitly set.)
- Updated ``Jcrop`` and ``jQuery`` dependencies.
- Moved docs to *Read the Docs*: https://django-image-cropping.readthedocs.org
