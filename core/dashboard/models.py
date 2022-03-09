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
