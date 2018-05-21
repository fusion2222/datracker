from djsingleton.models import SingletonModel
from django_extensions.db.models import TimeStampedModel

from django.contrib.auth.models import User, AbstractUser
from django.db import models
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
        return '<IssueCategory #{} {}>'.format(self.pk, self.name)


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
