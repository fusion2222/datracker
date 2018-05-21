from django.contrib import admin
from django.urls import path

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth.decorators import login_required, permission_required
from .views import IndexView, IssueView, LoginView, LogoutView, PageView


urlpatterns = [
    path('admin/', admin.site.urls),

    # Custom Authentication
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),

    # Page paths
    path('', IndexView.as_view(), name='index'),
    path('<slug>/', PageView.as_view(), name='page-detail'),
    path('issue/<int:pk>', login_required(IssueView.as_view()), name='issue-update'),
]

urlpatterns += staticfiles_urlpatterns()