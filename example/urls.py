from django.conf import settings
from django.conf.urls import include, static, url
from django.contrib import admin
from example import views


urlpatterns = [
    url(r'^$', views.thumbnail_options,
        name='thumbnail_options'),
    url(r'^show_foreignkey_thumbnail/$',
        views.thumbnail_foreign_key,
        name='thumbnail_foreign_key'),
    url(r'^show_foreignkey_thumbnail/(?P<instance_id>\d+)/$',
        views.thumbnail_foreign_key,
        name='thumbnail_foreign_key'),
    url(r'^modelform_example/(?P<image_id>\d+)/$',
        views.modelform_example,
        name='modelform_example'),
    url(r'^modelform_example/$',
        views.modelform_example,
        name='modelform_example'),
    url(r'^show_thumbnail/(?P<image_id>\d+)/$',
        views.show_thumbnail,
        name='show_thumbnail'),
    url(r'^admin/', admin.site.urls),
]

urlpatterns += static.static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
