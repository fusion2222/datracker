from django.contrib import admin
from django.urls import path

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth.decorators import login_required, permission_required
from .views import (
    EmployeeView, EmployeeCreateView, EmployeeDeleteView, IndexView, IssueView, IssueCreateView, IssueDeleteView, LoginView, LogoutView, PageView,
)


urlpatterns = [
    path('admin/', admin.site.urls),

    # Custom Authentication
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),

    # Page paths
    path('', IndexView.as_view(), name='index'),
    path('<slug>/', PageView.as_view(), name='page-detail'),

    path('issue/<int:pk>', login_required(IssueView.as_view()), name='issue-update'),
    path('issue/delete/<int:pk>', IssueDeleteView.as_view(), name='issue-delete'),
    path('issue/new', IssueCreateView.as_view(), name='issue-create'),

    path('employee/<int:pk>', login_required(EmployeeView.as_view()), name='employee-update'),
    path('employee/delete/<int:pk>', EmployeeDeleteView.as_view(), name='employee-delete'),
    path('employee/new', EmployeeCreateView.as_view(), name='employee-create'),
]

urlpatterns += staticfiles_urlpatterns()