from django.db import models
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser


import random
import string

from dashboard.models import Wallet

from .manager import AccountManager
from core.util.constants import Status


class Account(AbstractBaseUser, PermissionsMixin):
    '''
    Custom user model that supports using email instead of username
    '''
    def generate_random_text_id():
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))

    email = models.EmailField(max_length=255, unique=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    photo = models.ImageField(upload_to='profile_pics', blank=True)

    location = models.CharField(max_length=255, null=True, blank=True)
    customer_merchant_id = models.CharField(
        max_length=255, default=generate_random_text_id)
    wallet = models.OneToOneField(
        Wallet, on_delete=models.CASCADE, null=True, blank=True)
    # eg pending, approved, rejected
    labourer_status = models.CharField(
        max_length=50, default=Status.PENDING.value)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    is_labourer = models.BooleanField(default=False)

    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    objects = AccountManager()

    USERNAME_FIELD = 'email'

    class Meta:
        db_table = 'accounts'

        permissions = [
            ('disable_account', 'Can disable account'),
        ]

    def __str__(self):
        return self.name
