import decimal
import random
import string
import time
import uuid

from django.db import models

from core.util.constants import Disbursement, Status


class Service(models.Model):
    '''Services are jobs.'''
    def generate_job_id():
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    job_id = models.CharField(
        max_length=12, default=generate_job_id(), unique=False)
    customer = models.ForeignKey(
        'accounts.Account', on_delete=models.CASCADE, null=True, related_name='requested')
    labourer = models.ForeignKey(
        'accounts.Account', on_delete=models.CASCADE, null=True, related_name='doer')
    service_name = models.CharField(max_length=200)
    service_description = models.TextField(null=True, blank=True)
    charge = models.DecimalField(max_digits=10, decimal_places=3)
    mode_of_payment = models.CharField(max_length=20)
    status = models.CharField(max_length=20, default=Status.PENDING.value)
    published = models.BooleanField(default=False)
    accepted = models.BooleanField(default=False)   # determines whether labourer has accepted...
    date_of_service = models.DateTimeField(auto_now_add=True)
    date_of_completion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.service_name

    @property
    def get_service_rendered(self):
        service = f'Labourer: {self.labourer.name} rendered service: {self.service_name} for Cusomter: {self.customer.name} for the amount of: {self.charge}'
        return service


class Product(models.Model):
    name = models.CharField(verbose_name="Product Name", max_length=100)
    image = models.ImageField(
        verbose_name="Product Image", upload_to="product/", null=True, blank=True)
    min_price = models.DecimalField(
        verbose_name="Minimum Price", decimal_places=3, max_digits=10)
    max_price = models.DecimalField(
        verbose_name="Maximum Price", decimal_places=3, max_digits=10)

    def __str__(self):
        return self.name


class Wallet(models.Model):

    wallet_id = models.CharField(
        verbose_name="Wallet ID", max_length=100, default=uuid.uuid4)
    holder = models.ForeignKey(
        'accounts.Account', on_delete=models.CASCADE, null=True, related_name='account_holder')
    main_balance = models.DecimalField(
        verbose_name="Main Balance", decimal_places=2, max_digits=50, default=0.0)
    available_balance = models.DecimalField(
        verbose_name="available Balance", decimal_places=2, max_digits=50, default=0.0)
    date_added = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def credit_available_balance(self, amount):
        self.available_balance += decimal.Decimal(amount)
        self.save()

    def debit_available_balance(self, amount):
        self.available_balance -= decimal.Decimal(amount)
        self.save()

    def credit_main_balance(self, amount):
        self.main_balance += decimal.Decimal(amount)
        self.save()

    def debit_main_balance(self, amount):
        self.main_balance -= decimal.Decimal(amount)
        self.save()

    def credit_wallet(self, amount):
        self.main_balance += decimal.Decimal(amount)
        self.available_balance += decimal.Decimal(amount)
        self.save()

    def debit_wallet(self, amount):
        self.main_balance -= decimal.Decimal(amount)
        self.available_balance -= decimal.Decimal(amount)
        self.save()

    def get_wallet_balance(self):
        return decimal.Decimal(self.main_balance)

    def __str__(self):
        return self.wallet_id


class Disbursement(models.Model):
    wallet = models.ForeignKey(
        Wallet, on_delete=models.CASCADE, null=True, blank=True, related_name='disbursement')
    amount = models.DecimalField(
        decimal_places=2, max_digits=50, default=0.0)
    note = models.TextField(null=True, blank=True)
    disburser = models.ForeignKey(
        'accounts.Account', on_delete=models.CASCADE, null=True, related_name='disburser')
    date_of_disbursement = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(
        'accounts.Account', on_delete=models.CASCADE, null=True, related_name='modified_by')
    disbursement_type = models.CharField(max_length=200, blank=True, null=True)
    status = models.CharField(max_length=200, default=Status.PENDING.value)
    reason = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.wallet.wallet_id

    class Meta:
        db_table = 'disbursements'


class Transaction(models.Model):
    def generate_transaction_id():
        time_id = str(int(time.time() * 100))
        return time_id.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    transaction_id = models.CharField(
        verbose_name="Wallet ID", max_length=50, default=generate_transaction_id)
    customer = models.ForeignKey(
        'accounts.Account', on_delete=models.CASCADE, related_name='customer')
    network = models.CharField(max_length=20, default='MTN')
    from_phone = models.CharField(max_length=15, blank=True)
    labourer = models.ForeignKey(
        'accounts.Account', on_delete=models.CASCADE, verbose_name="Labourer")
    amount = models.DecimalField(
        verbose_name="Amount", decimal_places=3, max_digits=10)
    payment_mode = models.CharField(
        verbose_name="Mode of Payment", default='MOMO', max_length=50)
    service = models.CharField(verbose_name="Service Rendered", max_length=50)
    note = models.CharField(max_length=500, blank=True)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, null=True)
    payment_status = models.CharField(
        verbose_name="Payment Status", max_length=50)
    payment_status_code = models.CharField(max_length=10, default='001')
    payment_date = models.DateTimeField(
        verbose_name="Payment date", auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.transaction_id

    class Meta:
        db_table = 'transactions'
        permissions = [
            ('make_payment', 'Can Make Payment'),
            ('receive_payment', 'Can Receive Payment'),
        ]


class JobCategory(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(
        verbose_name="Category Image", upload_to="category/", null=True, blank=True)
    published = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
