from django.conf.urls import patterns, include, url, static
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'views.form'),
    url(r'^admin/', include(admin.site.urls)),

)
urlpatterns += static.static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
