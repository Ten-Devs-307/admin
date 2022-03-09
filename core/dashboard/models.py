from django.db import models

class Product(models.Model):
   name = models.CharField(verbose_name="Product")

class Wallet(models.Model):
   wallet_id = models.CharField(verbose_name="Wallet ID", max_length=50)
   main_balance = models.DecimalField(verbose_name="Main Balance")
   available_balance = models.DecimalField(verbose_name="available Balance")
   
   def __str__(self):
       return self.wallet_id
   
   
class Transaction(models.Model):
   transaction_id = models.CharField(verbose_name="Wallet ID", max_length=50)
   customer = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name="Customer")
   labourer = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name="Labourer")
   amount = models.DecimalField(verbose_name="Amount")
   payment_mode = models.CharField(verbose_name="Mode of Payment", max_length=50)
   service = models.CharField(verbose_name="Service Rendered", max_length=50)
   wallet = models.ForeignKey(Wallet, on_delete=models.SET_NULL)
   payment = models.CharField(verbose_name="Payment Status", max_length=50)
   payment_date = models.DateTimeField(verbose_name="Payment date")
   
   def __str__(self):
       return self.transaction_id
   
   