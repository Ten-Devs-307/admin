import random
import string

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from core.util.constants import Status
from dashboard.models import Wallet

from .manager import AccountManager


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
        max_length=255, default=generate_random_text_id)  # unique id for various usercategories
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
            ('change_account_status', 'Can Change Status Of Account'),
            ('view_customer', 'Can View Customer'),
            ('view_labourer', 'Can View Labourer'),
            ('view_admin', 'Can View Admins'),
            ('delete_labourer', 'Can Delete Labourer'),
            ('delete_admin', 'Can Delete Staff Member'),
            ('delete_customer', 'Can Delete Customer'),
            ('change_admin', 'Can Change Admin Status'),
        ]

    def __str__(self):
        '''In the case where user is not having a name, we return email'''
        return self.name if self.name else self.email
