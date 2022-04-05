from email.policy import default
from django.db import models
from accounts.models import Account
# Create your models here.


class Service(models.Model):
    customer = models.ForeignKey(
        Account, on_delete=models.CASCADE, null=True, related_name='requested')
    labourer = models.ForeignKey(
        Account, on_delete=models.CASCADE, null=True, related_name='doer')
    service_name = models.CharField(max_length=200)
    service_description = models.TextField(null=True, blank=True)
    charge = models.DecimalField(max_digits=10, decimal_places=3)
    mode_of_payment = models.CharField(max_length=200)
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
    wallet_id = models.CharField(verbose_name="Wallet ID", max_length=50)
    main_balance = models.DecimalField(
        verbose_name="Main Balance", decimal_places=3, max_digits=10)
    available_balance = models.DecimalField(
        verbose_name="available Balance", decimal_places=3, max_digits=10)

    def __str__(self):
        return self.wallet_id


class Transaction(models.Model):
    transaction_id = models.CharField(verbose_name="Wallet ID", max_length=50)
    customer = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name='customer')
    network = models.CharField(max_length=20, default='MTN')
    from_phone = models.CharField(max_length=15, blank=True)
    labourer = models.ForeignKey(
        Account, on_delete=models.CASCADE, verbose_name="Labourer")
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
