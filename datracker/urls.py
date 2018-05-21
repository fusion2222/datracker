from django.contrib import admin
from django.urls import path

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from .views import IndexView, LoginView, LogoutView, PageView


urlpatterns = [
    path('admin/', admin.site.urls),

    # Custom Authentication
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),

    # Page paths
    path('', IndexView.as_view(), name='index'),
    path('<slug>/', PageView.as_view(), name='page-detail'),
]

urlpatterns += staticfiles_urlpatterns()