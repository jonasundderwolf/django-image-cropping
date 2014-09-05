from __future__ import unicode_literals
from django.core.files import File
from django.conf import settings
from django.contrib.auth.models import User
from PIL import Image, ImageDraw
from example.models import Image as TestImage


def create_cropped_image(**kwargs):
    defaults = {
        'image_cropping': '50,50,170,100',  # size: 120x100  as in model.py
        'image_path': '%s%s' % (settings.STATIC_ROOT, "/images/example_image.jpg"),
        'image_name': 'example_image',
    }
    defaults.update(kwargs)
    image = TestImage.objects.create(
        **{'cropping': defaults['image_cropping']}
    )
    image.image_field.save(
        defaults['image_name'],
        File(open(defaults['image_path'], 'rb')))
    return image


def create_pil_image(size=(400, 400)):
    image = Image.new('RGB', size, (255, 255, 255))
    draw = ImageDraw.Draw(image)
    draw.rectangle(((20, 20), (200, 200)), fill="red", outline="black")
    draw.rectangle(((220, 220), (390, 390)), fill="green", outline="black")
    draw.ellipse((100, 100, 310, 310), fill="yellow", outline="black")
    return image


def create_superuser(**kwargs):
    defaults = {
        'password': 'admin',
        'username': 'admin',
        'email': 'admin@admin.test',
    }
    defaults.update(kwargs)
    return User.objects.create_superuser(**defaults)
