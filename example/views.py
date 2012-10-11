from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from easy_thumbnails.files import get_thumbnailer
from .models import Image, ImageFK
from .forms import ImageForm


def thumbnail_options(request):
    try:
        image = Image.objects.all()[0]
    except (Image.DoesNotExist, IndexError,):
        image = None
    return render(request, 'thumbnail_options.html', {'image': image})


def thumbnail_foreign_key(request, instance_id=None):
    if not instance_id:
        try:
            imagefk = ImageFK.objects.all()[0]
        except (ImageFK.DoesNotExist, IndexError,):
            imagefk = None
    else:
        try:
            imagefk = ImageFK.objects.get(pk=instance_id)
        except ImageFK.DoesNotExist:
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


def modelform_example(request, image_id=None):
    image = get_object_or_404(Image, pk=image_id) if image_id else None
    form = ImageForm(instance=image)
    if request.method == "POST":
        form = ImageForm(request.POST, request.FILES, instance=image)
        if form.is_valid():
            image = form.save()
            return HttpResponseRedirect(reverse('modelform_example', args=(image.pk,)))
    return render(request, 'modelform_example.html', {'form': form, 'image': image})
