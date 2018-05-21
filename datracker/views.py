from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views.generic.base import RedirectView
from django.views.generic.edit import FormView

from datracker.forms import LoginForm
from datracker.enums import Pages
from datracker.models import Page


class LoginView(FormView):
    template_name = 'auth/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('index')
    success_message = "%(first_name)s %(last_name)s is logged in!"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs


class LogoutView(RedirectView):
    permanent = False
    query_string = False
    pattern_name = 'index'

    def get_redirect_url(self, *args, **kwargs):

        if self.request.user.is_authenticated:
            logout(self.request)

        return super().get_redirect_url(*args, **kwargs)


class IndexView(RedirectView):
    permanent = False
    query_string = True
    pattern_name = 'page-detail'

    def get_redirect_url(self, *args, **kwargs):
        page_pk = Pages.DASHBOARD if self.request.user else Pages.ABOUT
        kwargs.update(
            Page.objects.filter(pk=page_pk).values('slug').first()
        )

        return super().get_redirect_url(*args, **kwargs)


class PageView(DetailView):
    model = Page
    template_name = 'pages/base.html'

    def get_object(self, *args, **kwargs):
        object = super().get_object(*args, **kwargs)

        if object.pk == Pages.ABOUT:
            self.template_name = 'pages/index.html'

        return object
