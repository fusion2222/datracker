from django.contrib.auth.models import User, AbstractUser
from django.db import models


class Employee(AbstractUser):

    AVATAR_HEIGHT = 53
    AVATAR_WIDTH = 53

    avatar = models.ImageField(upload_to='avatars')
    email = models.EmailField(unique=True)
