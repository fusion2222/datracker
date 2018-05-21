from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView
from django.views.generic.base import RedirectView
from django.views.generic.edit import DeleteView, FormView, UpdateView

from django.http import Http404, HttpResponseRedirect

from datracker.forms import LoginForm
from datracker.enums import Pages
from datracker.models import Issue, Page


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
        page_pk = Pages.DASHBOARD if self.request.user.is_authenticated else Pages.ABOUT
        kwargs.update(
            Page.objects.filter(pk=page_pk).values('slug').first()
        )

        return super().get_redirect_url(*args, **kwargs)


class PageView(DetailView):
    model = Page
    template_name = 'pages/base.html'

    def get_object(self, *args, **kwargs):
        page = super().get_object(*args, **kwargs)

        if not page.can_be_seen_by(self.request.user):
            raise Http404('Page is not found')

        return page

    def get_context_data(self, *args, **kwargs):

        context = super().get_context_data(*args, **kwargs)

        if self.object.pk == Pages.ABOUT:
            self.template_name = 'pages/index.html'
        elif self.object.pk == Pages.ISSUES:
            self.template_name = 'issues/list.html'
            context['issues'] = Issue.objects.all().order_by('-created')

        return context


class IssueView(UpdateView):
    model = Issue
    template_name = 'issues/update.html'
    fields = ['name', 'description', 'assignee', 'category']

    def get_form(self, *args, **kwargs):

        # can_be_solved_by
        output = super().get_form(*args, **kwargs)

        if not self.request.user.has_perm('can_change_issue'):
            for field_name, field in output.fields.items():
                field.disabled = True

        return output

    def post(self, *args, **kwargs):

        if 'resolve' in self.request.POST:
            messages.add_message(self.request, messages.WARNING, 'Issue resolution is not yet working. Coming on soon.')

        return super().post(*args, **kwargs)


class IssueDeleteView(PermissionRequiredMixin, DeleteView):
    model = Issue
    template_name = 'issues/delete.html'
    permission_required = 'datracker.delete_issue'

    def get_success_url(self, *args, **kwargs):
        page_kwargs = Page.objects.filter(pk=Pages.ISSUES).values('slug').first()
        return reverse('page-detail', kwargs=page_kwargs)