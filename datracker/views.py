from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView
from django.views.generic.base import RedirectView
from django.views.generic.edit import CreateView, DeleteView, FormView, UpdateView

from datracker.forms import LoginForm
from datracker.enums import Pages
from datracker.models import Issue, Page, Employee


class LoginView(FormView):
    template_name = 'auth/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('index')
    success_message = "%(first_name)s %(last_name)s is logged in!"

    def get_form_kwargs(self):
        """
        LoginForm needs to have a request in order to make authentication.
        In this function request is sent to LoginForm.
        """
        kwargs = super().get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs


class LogoutView(LoginRequiredMixin, RedirectView):
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
        """
        If visited as unauthenticated, we shoukld show About page. Otherwise Dashboard page.
        """
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

        # Most of pages are visible only for logged users.
        if not page.can_be_seen_by(self.request.user):
            raise Http404('Page is not found')

        return page

    def get_context_data(self, *args, **kwargs):
        """
        If any page needs any special content or template,
        this is where it should be handled.
        """
        context = super().get_context_data(*args, **kwargs)

        self.template_name = self.object.get_specific_template_name(
            default=self.template_name
        )

        context.update(self.object.get_additional_context())

        return context


class IssueView(LoginRequiredMixin, UpdateView):
    model = Issue
    template_name = 'issues/update.html'
    fields = ['name', 'solved', 'description', 'assignee', 'category']

    def get_form(self, *args, **kwargs):
        """
        Ordinary Employees can see an Issue, however they cannot to edit it. In case
        Employee is not privileged, form will be returned to him, but disabled.
        """
        output = super().get_form(*args, **kwargs)

        if not self.request.user.has_perm('can_change_issue'):
            for field_name, field in output.fields.items():
                field.disabled = True

        return output

    def post(self, *args, **kwargs):
        """
        TODO: In future, Employees will be able to set save 'ended' date,
        if the Issue is assigned to them.
        """
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


class IssueCreateView(PermissionRequiredMixin, CreateView):
    model = Issue
    template_name = 'issues/create.html'
    permission_required = 'datracker.create_issue'
    fields = ['name', 'description', 'assignee', 'category']

    def get_success_url(self, *args, **kwargs):
        page_kwargs = Page.objects.filter(pk=Pages.ISSUES).values('slug').first()
        return reverse('page-detail', kwargs=page_kwargs)


class EmployeeView(LoginRequiredMixin, UpdateView):
    model = Employee
    template_name = 'employees/profile.html'
    fields = ['first_name', 'last_name', 'avatar', 'email', 'password']


class EmployeeCreateView(LoginRequiredMixin, CreateView):
    model = Employee
    xyz = 321


class EmployeeDeleteView(LoginRequiredMixin, DeleteView):
    model = Employee
    xyz = 321
