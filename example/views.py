from django.shortcuts import render, get_object_or_404
from forms import ImageForm
from models import Image, ImageFK


def form(request):
    try:
        image = Image.objects.all()[0]
        form = ImageForm(instance=image)
    except (Image.DoesNotExist, IndexError,):
        image = None
        form = ImageForm

    try:
        imagefk = ImageFK.objects.all()[0]
    except (ImageFK.DoesNotExist, IndexError,):
        imagefk = None

    return render(request, 'form.html', {'form': form, 'image': image, 'imagefk': imagefk})


def show_thumbnail(request, image_id):
    image = get_object_or_404(Image, pk=image_id)
    from easy_thumbnails.files import get_thumbnailer
    thumbnail_url = get_thumbnailer(image.image_field).get_thumbnail({
        'size': (430, 360),
        'box': image.cropping,
        'crop': True,
        'detail': True,
    }).url
    return render(request, 'thumbnail.html', {'thumbnail_url': thumbnail_url})
