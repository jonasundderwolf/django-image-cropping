from django.shortcuts import render
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
