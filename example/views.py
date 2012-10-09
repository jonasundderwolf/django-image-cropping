from django.shortcuts import render, get_object_or_404
from easy_thumbnails.files import get_thumbnailer
from .models import Image, ImageFK


def thumbnail_options(request):
    try:
        image = Image.objects.all()[0]
    except (Image.DoesNotExist, IndexError,):
        image = None
    return render(request, 'thumbnail_options.html', {'image': image})


def thumbnail_foreign_key(request):
    try:
        imagefk = ImageFK.objects.all()[0]
    except (ImageFK.DoesNotExist, IndexError,):
        imagefk = None
    return render(request, 'thumbnail_foreign_key.html', {'imagefk': imagefk})


def show_thumbnail(request, image_id):
    image = get_object_or_404(Image, pk=image_id)
    thumbnail_url = get_thumbnailer(image.image_field).get_thumbnail({
        'size': (430, 360),
        'box': image.cropping,
        'crop': True,
        'detail': True,
    }).url
    return render(request, 'thumbnail.html', {'thumbnail_url': thumbnail_url})
