from example import views

from django.conf import settings
from django.conf.urls import static
from django.contrib import admin
from django.urls import re_path

urlpatterns = [
    re_path(r"^$", views.thumbnail_options, name="thumbnail_options"),
    re_path(
        r"^show_foreignkey_thumbnail/$",
        views.thumbnail_foreign_key,
        name="thumbnail_foreign_key",
    ),
    re_path(
        r"^show_foreignkey_thumbnail/(?P<instance_id>\d+)/$",
        views.thumbnail_foreign_key,
        name="thumbnail_foreign_key",
    ),
    re_path(
        r"^modelform_example/(?P<image_id>\d+)/$",
        views.modelform_example,
        name="modelform_example",
    ),
    re_path(r"^modelform_example/$", views.modelform_example, name="modelform_example"),
    re_path(
        r"^show_thumbnail/(?P<image_id>\d+)/$",
        views.show_thumbnail,
        name="show_thumbnail",
    ),
    re_path(r"^admin/", admin.site.urls),
]

urlpatterns += static.static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
