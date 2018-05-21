from django.contrib import admin
from django.urls import path

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from .views import IndexView, LogoutView, PageView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('logout', LogoutView.as_view(), name='logout'),
    path('', IndexView.as_view(), name='index'),
    path('<slug>/', PageView.as_view(), name='page-detail'),
]

urlpatterns += staticfiles_urlpatterns()