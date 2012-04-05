from django.shortcuts import render
from forms import ImageForm
from models import Image


def form(request):
    image = Image.objects.all()[0]
    form = ImageForm(instance=image)

    return render(request, 'form.html', {'form': form, 'image': image})
