from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser

from .manager import AccountManager


class Account(AbstractBaseUser, PermissionsMixin):
    '''
    Custom user model that supports using email instead of username
    '''
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)

    photo = models.ImageField(upload_to='profile_pics', blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    is_labourer = models.BooleanField(default=False)

    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    objects = AccountManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.name
