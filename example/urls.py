from django.conf import settings
from django.conf.urls import include, static, url
from django.contrib import admin


urlpatterns = [
    url(r'^$', 'example.views.thumbnail_options',
        name='thumbnail_options'),
    url(r'^show_foreignkey_thumbnail/$',
        'example.views.thumbnail_foreign_key',
        name='thumbnail_foreign_key'),
    url(r'^show_foreignkey_thumbnail/(?P<instance_id>\d+)/$',
        'example.views.thumbnail_foreign_key',
        name='thumbnail_foreign_key'),
    url(r'^modelform_example/(?P<image_id>\d+)/$',
        'example.views.modelform_example',
        name='modelform_example'),
    url(r'^modelform_example/$',
        'example.views.modelform_example',
        name='modelform_example'),
    url(r'^show_thumbnail/(?P<image_id>\d+)/$',
        'example.views.show_thumbnail',
        name='show_thumbnail'),
    url(r'^admin/', include(admin.site.urls)),
]

urlpatterns += static.static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
