django-image-cropping
=====================

``django-image-cropping`` is an app for cropping uploaded images via Django's admin backend using `imgareaselect 
<https://github.com/odyniec/imgareaselect>`_. It keeps the original image intact, only cropping when the image
is being displayed. Large images are presented in a small format, so even very big images can easily be cropped.

``django-image-cropping`` is perfect when you need images with a specific size for your templates but want your
users or editors to upload images of any dimension. It presents a selection with a fixed aspect ratio so your users
can't break the layout with oddly-sized images.

It provides the necessary fields, widgets and a (`easy_thumbnails 
<http://github.com/SmileyChris/easy-thumbnails>`_) thumbnail processor for displaying the 
cropped image in your templates. Also works with `FeinCMS <https://github.com/feincms/feincms>`_ content types!

Screenshot: 

.. image:: http://www.jonasundderwolf.de/media/uploads/judw_logo.png

Installation
------------

#. Install django-image-cropping using pip. For example::

    pip install django-image-cropping

#. Add ``easy_thumbnails`` and ``image_cropping`` to your INSTALLED_APPS. ``image_cropping`` is only required if you are using Django 1.3 and ``contrib.staticfiles``

#. Adjust the thumbnail processors for ``easy_thumbnails`` in your ``settings.py``::

    from easy_thumbnails import defaults
    THUMBNAIL_PROCESSORS = (
        'image_cropping.thumbnail_processors.crop_corners',
    ) + defaults.PROCESSORS

#. Deploy the necessary static files. If you are using Django 1.3 and ``contrib.staticfiles`` the 
   necessary static files should be picked up automatically. In all other cases you have to copy or
   symlink the static files. Depending on your setup the command should look similiar to this::

        ln -s ~/.virtualenvs/yourenv/src/django-image-cropping/image_cropping/static/image_cropping/

    

Configuration
-------------

In order to make a regular ImageField croppable, simply turn it into an ``ImageCropField``. Then add
an ``ImageRatioField``, which will contain the boundaries of the cropped image. The ``ImageRatioField``
expects the name of the associated ImageCropField as the first argument and the size of the final image
to be displayed as the second argument.

The size is passed in as a string and defines the aspect ratio of the selection as well as the minimum
size for the final image. You can configure a warning if users try to crop a selection smaller than this
size (see below).

#. Model fields and options::

    from image_cropping.fields import ImageRatioField, ImageCropField

    image = ImageCropField(blank=True, null=True, upload_to='uploaded_images')
    # size is "width x height"
    cropping = ImageRatioField('image', '430x360')

#. If your setup is correct you should automatically see the enhanced image widget that provides a selection
   area for the image in the admin backend. 

#. Example usage of the thumbnail processor::

    {% thumbnail yourmodel.image 430x360 box=yourmodel.cropping crop detail %}

#. Additionally you can define the maximum size of the preview thumbnail in your settings.py::

    # size is "width x height"
    IMAGE_CROPPING_THUMB_SIZE = (300, 300)

#. You can warn users about crop selections that are smaller than the size defined in the ImageRatioField.
   When users try to do a smaller selection, a red border appears around the image. To use this functionality,
   add the parameter to the ImageRatioField::

    cropping = ImageRatioField('image', '430x360', size_warning=True)

   You can enable this functionality project-wide by adding the following line to your settings file::

    IMAGE_CROPPING_SIZE_WARNING = True


Extras
------

If you need the same image in multiple formats, simply specify another ImageRatioField. This will allow the image to be cropped twice::

    from image_cropping.fields import ImageRatioField, ImageCropField

    image = ImageCropField(blank=True, null=True, upload_to='uploaded_images')
    # size is "width x height"
    list_page_cropping = ImageRatioField('image', '200x100')
    detail_page_cropping = ImageRatioField('image', '430x360')
 

In your templates, use the corresponding ratio field::

    {% thumbnail yourmodel.image 200x100 box=yourmodel.list_page_cropping crop detail %}


If you need to crop an image contained within another model, referenced by a ForeignKey, use a ``CropForeignKey``. This
field works like a regular ForeignKey but expects a keyword argument named ``field_name``. The model attribute with this
name needs to be an ImageField that will be cropped::

    from django.db import models
    from image_cropping.fields import ImageRatioField, CropForeignKey
    
    class Image(models.Model):
        image_field = models.ImageField(upload_to='image/')

    class NewsItem(models.Model):
        title = models.CharField(max_length=255)
        image = CropForeignKey(Image, 'image_field')
        cropping = ImageRatioField('image', '120x100')

The CropForeignKey works only in the admin for now, as it uses the ``raw_id`` widget.
