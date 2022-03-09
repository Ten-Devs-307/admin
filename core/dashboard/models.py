from django.db import models
from accounts.models import Account
# Create your models here.


class Service(models.Model):
    customer = models.ForeignKey(
        Account, on_delete=models.SET_NULL, null=True, related_name='customer')
    labourer = models.ForeignKey(
        Account, on_delete=models.SET_NULL, null=True, related_name='labourer')
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
    min_price = models.DecimalField(verbose_name="Minimum Price", )
    max_price = models.DecimalField(verbose_name="Maximum Price")

    def __str__(self):
        return self.name


class Wallet(models.Model):
    wallet_id = models.CharField(verbose_name="Wallet ID", max_length=50)
    main_balance = models.DecimalField(verbose_name="Main Balance")
    available_balance = models.DecimalField(verbose_name="available Balance")

    def __str__(self):
        return self.wallet_id


class Transaction(models.Model):
    transaction_id = models.CharField(verbose_name="Wallet ID", max_length=50)
    customer = models.ForeignKey(
        Account, on_delete=models.SET_NULL, verbose_name="Customer")
    labourer = models.ForeignKey(
        Account, on_delete=models.SET_NULL, verbose_name="Labourer")
    amount = models.DecimalField(verbose_name="Amount")
    payment_mode = models.CharField(
        verbose_name="Mode of Payment", max_length=50)
    service = models.CharField(verbose_name="Service Rendered", max_length=50)
    wallet = models.ForeignKey(Wallet, on_delete=models.SET_NULL)
    payment = models.CharField(verbose_name="Payment Status", max_length=50)
    payment_date = models.DateTimeField(verbose_name="Payment date")

    def __str__(self):
        return self.transaction_id
