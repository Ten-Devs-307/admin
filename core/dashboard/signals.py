from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import Account
from dashboard.models import Disbursement, Wallet


@receiver(post_save, sender=Account)
def create_wallet(sender, instance, created, **kwargs):
    '''Create a wallet for each new staff member. Also create a wallet for each approved labourer'''
    if created == True:
        if instance.is_staff or instance.is_superuser:
            wallet = Wallet.objects.create(holder=instance)
            wallet.save()
            instance.wallet = wallet
            instance.save()
            print('Wallet created for staff member')
    else:
        if instance.is_labourer or instance.is_staff or instance.is_superuser:
            if not instance.wallet:
                wallet = Wallet.objects.create(holder=instance)
                wallet.save()
                instance.wallet = wallet
                instance.save()
                print('Wallet created for labourer')
