django-image-cropping
=====================

``django-image-cropping`` is an app for cropping uploaded images via Django's admin backend using `imgareaselect 
<https://github.com/odyniec/imgareaselect>`_.

It provides the necessary fields, widgets and a (`easy_thumbnails 
<http://github.com/SmileyChris/easy-thumbnails>`_) thumbnail processor for displaying the 
cropped image in your templates. 

Installation
------------

#. Install the django-image-cropping using pip. For example::

    pip install -e git+ssh://git@github.com/anrie/django-image-cropping.git#egg=django-image-cropping

#. Add ``easy_thumbnails`` and ``image_cropping`` to your INSTALLED_APPS. ``image_cropping`` is only required if you are using Django 1.3 and ``contrib.staticfiles``

#. Adjust the thumbnail processors for ``easy_thumbnails`` in your ``settings.py``::

    from easy_thumbnails import defaults
    THUMBNAIL_PROCESSORS = (
        'image_cropping.thumbnail_processors.crop_corners',
    ) + defaults.PROCESSORS

#. Deploy the necessary static files::

   If you are using Django 1.3 and ``contrib.staticfiles`` the necessary static files should be picked up atomatically.
   In all other cases you have to copy or symlink the static files. Depending on your setup your command should look similiar to this::

       ln -s ~/.virtualenvs/yourenv/src/django-image-cropping/image_cropping/static/image_cropping/

    


Configuration
-------------

You have to add two fields to your model. An ``ImageCropField`` and an ``ImageRatioField``.
The ``ImageRatioField`` expects the name of the associated ImageCropField as first argument.
Optionally you can define the ratio, which also represents the minimal size: Once set, your selection area is locked to the defined value. If the image is too small, the maximum available area is used.

#. Model fields and options::

    from image_cropping.fields import ImageRatioField, ImageCropField

    image = ImageCropField(blank=True, null=True, upload_to='uploaded_images')
    cropping = ImageRatioField('image', '430x360')

#. If your setup is correct you should automatically see the enhanced image widget that provides a selection area for the image in the admin backend. 

    See: http://dl.dropbox.com/u/6900359/pselect.png

#. Example usage of the thumbnail processor::

    {% thumbnail yourmodel.image 195x195 box=yourmodel.cropping crop detail %}


#. Additionaly you can define the size of the preview thumbnail in your settings.py::

    IMAGE_CROPPING_THUMB_SIZE = (width, height)






