from __future__ import unicode_literals

import json
from django.http import HttpResponse, Http404
from django.conf.urls import patterns, url
from . import utils


class ImageCroppingMixin(object):
    def get_urls(self):
        urls = super(ImageCroppingMixin, self).get_urls()
        my_urls = patterns(
            '',
            url(r'(\d+)/cropping_thumbnail/([^\/]+)/$',
                self.admin_site.admin_view(self.generate_thumbnail)),
        )
        return my_urls + urls

    def generate_thumbnail(self, request, pk, imagepath):
        obj = self.model.objects.get(pk=pk)
        image = obj
        for field in imagepath.split('__'):
            image = getattr(obj, field, None)
            if not image:
                raise Http404()

        data = utils.thumbnail_attrs(image)
        if not data:
            raise Http404()

        return HttpResponse(content=json.dumps(data),
                            content_type='application/json')
