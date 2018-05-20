from djsingleton.models import SingletonModel

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
