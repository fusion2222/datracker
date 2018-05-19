from django.contrib import admin
from django.urls import path

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from .views import index


urlpatterns = [
    path('', index),
    path('admin/', admin.site.urls),
]

urlpatterns += staticfiles_urlpatterns()