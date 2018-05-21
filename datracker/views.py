from datetime import timedelta

from django.db.models import Avg, Count, F, IntegerField, Max, Min, ExpressionWrapper
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView
from django.views.generic.base import RedirectView
from django.views.generic.edit import CreateView, DeleteView, FormView, UpdateView

from django.http import Http404, HttpResponseRedirect

from datracker.forms import LoginForm
from datracker.enums import Pages
from datracker.models import Issue, Page, Employee


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

    def get_dashboard_stats(self):
        """
        This method returns aggregation used for dashboard.
        :return: dictionary
        """
        output = {}

        issues = Issue.objects.exclude(solved__isnull=True).annotate(
            solving_time_duration=ExpressionWrapper(
                # Note: We cant use DurationField here! SQLlite can not run Avg on it.
                # Casting duration into IntegerField converts our data to microseconds.
                F('solved') - F('created'), output_field=IntegerField()
            )
        )

        output.update(
            issues.aggregate(avg_solving_duration=Avg('solving_time_duration'))
        )

        output.update(
            issues.aggregate(max_solving_duration=Max('solving_time_duration'))
        )

        output.update(
            issues.aggregate(min_solving_duration=Min('solving_time_duration'))
        )

        for key, value in output.items():
            duration = timedelta(seconds=round(value / 1000000))
            output[key] = str(duration)

        employees = Employee.objects.annotate(solved_issues_count=Count('issue'))

        output.update(
            employees.aggregate(max_issues_assigned=Max('solved_issues_count'))
        )

        output.update(
            employees.aggregate(min_issues_assigned=Min('solved_issues_count'))
        )

        output.update(
            employees.aggregate(avg_issues_assigned=Avg('solved_issues_count'))
        )

        output.update(
            {
                'total_unresolved_issues': Issue.objects.filter(solved__isnull=True).count(),
                'total_resolved_issues': Issue.objects.filter(solved__isnull=False).count(),
            }
        )
        return output

    def get_context_data(self, *args, **kwargs):

        context = super().get_context_data(*args, **kwargs)

        if self.object.pk == Pages.ABOUT:
            self.template_name = 'pages/index.html'
        if self.object.pk == Pages.DASHBOARD:
            self.template_name = 'pages/dashboard.html'
            context.update(self.get_dashboard_stats())
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

class IssueCreateView(PermissionRequiredMixin, CreateView):
    model = Issue
    template_name = 'issues/create.html'
    permission_required = 'datracker.create_issue'
    fields = ['name', 'description', 'assignee', 'category']

    def get_success_url(self, *args, **kwargs):
        page_kwargs = Page.objects.filter(pk=Pages.ISSUES).values('slug').first()
        return reverse('page-detail', kwargs=page_kwargs)