from djsingleton.models import SingletonModel
from django_extensions.db.models import TimeStampedModel

from django.contrib.auth.models import User, AbstractUser
from django.db import models


class Employee(AbstractUser):

    AVATAR_HEIGHT = 53
    AVATAR_WIDTH = 53

    avatar = models.ImageField(upload_to='avatars')
    email = models.EmailField(unique=True)

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

    def __str__(self):
        return '<{} #{} {}>'.format(
            self.__class__.__name__, self.pk, self.title[:20]
        )