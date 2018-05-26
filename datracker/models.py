from datetime import timedelta

from djsingleton.models import SingletonModel
from django_extensions.db.models import TimeStampedModel

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User, AbstractUser
from django.db import models
from django.db.models import Avg, Count, F, IntegerField, Max, Min, ExpressionWrapper
from django.urls import reverse

from datracker.enums import Pages


class Employee(AbstractUser):

    AVATAR_HEIGHT = 53
    AVATAR_WIDTH = 53

    avatar = models.ImageField(upload_to='avatars')
    email = models.EmailField(unique=True)

    @property
    def name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    class Meta:
        # We need to override inherited User verbose_name.
        verbose_name = 'Employee'

    def __str__(self):
        return self.name

class SiteSettings(SingletonModel):
    # TODO: performance can be optimized using caching.

    site_name = models.CharField(max_length=150)
    site_slogan = models.CharField(max_length=150)

    def __str__(self):
        return '<{} #{} {}>'.format(
            self.__class__.__name__, self.pk, self.site_name
        )


class Page(TimeStampedModel):

    public_pages = [Pages.ABOUT, Pages.FAQ]

    title = models.CharField(
        max_length=150, help_text='Main title displayed on top of each page', default=''
    )
    label = models.CharField(
        max_length=150, help_text='Is displayed for example in navbar or links', default=''
    )
    meta_title = models.CharField(
        max_length=150, help_text='Title used only for social networks and search engines.', default=''
    )
    meta_description = models.TextField(
        max_length=200,
        help_text='Description used only for social networks and search engines.',
        default=''
    )
    content = models.TextField(default='')
    slug = models.SlugField(
        max_length=50, help_text='Specifies name of page in URL address.', unique=True
    )

    @property
    def is_private(self):
        """
        Checks if Page should be visible by anonymous users.
        Beware, Login and Logout subpages do not count here.
        """
        return self.pk not in self.public_pages

    _specific_templates = {
        Pages.ABOUT: 'pages/index.html',
        Pages.DASHBOARD: 'pages/dashboard.html',
        Pages.ISSUES: 'issues/list.html'
    }

    def get_specific_template_name(self, default):
        return self._specific_templates.get(self.pk, default)

    def _get_dashboard_page_issue_data(self):
        """
        Appends Issue aggregates for dashboard to output.
        """
        output = {}

        issues = Issue.objects.exclude(solved__isnull=True).annotate(
            solving_time_duration=ExpressionWrapper(
                # We cant use DurationField here! SQLlite can not run Avg on it.
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
            # IntegerField from aggregation returned microseconds. They are converted here
            # into seconds, and round them so we dont have output like 2 Days 12:14:063423...
            duration = timedelta(seconds=round(value / 1000000))
            output[key] = str(duration)

        return output

    def _get_dashboard_page_employee_data(self):
        """
        Appends Employee aggregates for dashboard to output.
        """
        output = {}

        employees = get_user_model().objects.annotate(solved_issues_count=Count('issue'))

        output.update(
            employees.aggregate(max_issues_assigned=Max('solved_issues_count'))
        )

        output.update(
            employees.aggregate(min_issues_assigned=Min('solved_issues_count'))
        )

        output.update(
            employees.aggregate(avg_issues_assigned=Avg('solved_issues_count'))
        )

        return output

    def get_dashboard_stats(self):
        """
        This method returns all aggregate data used for dashboard.
        :return: dictionary
        """
        output = {}

        output.update(
            self._get_dashboard_page_issue_data()
        )
        output.update(
            self._get_dashboard_page_employee_data()
        )
        output.update(
            {
                'total_unresolved_issues': Issue.objects.filter(solved__isnull=True).count(),
                'total_resolved_issues': Issue.objects.filter(solved__isnull=False).count(),
            }
        )
        return output

    def get_additional_context(self):

        if self.pk == Pages.DASHBOARD:
            return self.get_dashboard_stats()

        elif self.pk == Pages.ISSUES:
            return {
                'issues': Issue.objects.all().order_by('-created')
            }
        else:
            return {}

    def can_be_seen_by(self, user):
        return not self.is_private or user.is_authenticated and self.is_private

    def get_absolute_url(self):
        return reverse('page-detail', kwargs={'slug': self.slug})

    def __str__(self):
        return '<{} #{} {}>'.format(
            self.__class__.__name__, self.pk, self.title[:20]
        )


class IssueCategory(TimeStampedModel):
    name = models.CharField(
        max_length=150, help_text='Category name', default=''
    )
    description = models.TextField(
        max_length=200,
        help_text='Larger descriptive text about category.',
        default=''
    )

    class Meta:
        verbose_name_plural = "Issue Categories"

    def __str__(self):
        return '{}'.format(self.name)


class Issue(TimeStampedModel):
    name = models.CharField(
        max_length=150, help_text='Category name', default=''
    )
    description = models.TextField(
        max_length=800,
        help_text='Larger descriptive text about Issue',
        default=''
    )
    category = models.ForeignKey(
        'IssueCategory',
        on_delete=models.CASCADE,
    )
    assignee = models.ForeignKey(
        'Employee',
        on_delete=models.CASCADE,
    )
    solved = models.DateTimeField(help_text='Indicates when issue was solved.', null=True)

    def get_absolute_url(self):
        return reverse('issue-update', kwargs={'pk': self.pk})

    def get_delete_url(self):
        return reverse('issue-delete', kwargs={'pk': self.pk})

    def can_be_solved_by(self, employee):
        return not self.is_solved and employee.perms and self.request.user.has_perm('can_change_issue')

    @property
    def is_solved(self):
        """
        Currently are conditions simple. However in future it may change.
        """
        return self.solved is not None

    def __str__(self):
        return '<Issue #{} {}>'.format(self.pk, self.name)

    class Meta:
        permissions = (
            ('close_issue', 'Can close unfinished issue assigned to self'),
        )
